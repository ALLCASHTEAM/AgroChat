from fastapi import FastAPI, Request, Response, BackgroundTasks, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import json
import hashlib
import os
import aiofiles
from AI_PRO_MAX import mainAI
from hashlib import sha256

app = FastAPI()
with open('tmp.txt', 'w', encoding='utf-8') as f:
    f.write('-')
    f.write('-')
    f.write('-')
app.mount("/static", StaticFiles(directory="static"), name="static")
images_directory = os.path.join(os.getcwd(), "static/user_images")
app.mount("/static/user_images", StaticFiles(directory=images_directory), name="/static/user_images")


@app.get("/")
async def read_root():
    # You can specify the HTML file you want to render here
    return FileResponse("static/index.html")


@app.post("/request")
async def make_response(background_tasks: BackgroundTasks, text: str = Form(...), image: UploadFile = File(None)):
    text = mainAI.AI_COMPIL(text)

    if image:
        ext = image.filename.split('.')[-1]
        image_data = await image.read()
        hashed_image = sha256(image_data).hexdigest()
        filename = f'{hashed_image}.{ext}'

        file_path = f'static/user_images/{filename}'
        if filename not in os.listdir('static/user_images'):
            background_tasks.add_task(save_image, image_data, file_path)

    return {"text": text, "image": None}


async def save_image(image_data, file_path):
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(image_data)


@app.post("/get_image_hash")
async def get_image_hash(data: Request):
    body = await data.form()
    ext = body['image'].filename.split('.')[-1]
    image = await body['image'].read()
    hashed_image = hashlib.sha256(image).hexdigest()
    filename = f'{str(hashed_image)}.{ext}'
    return Response(content=json.dumps({'imageName': filename}), media_type="application/json")
