from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import json
import hashlib
import os
import time
from AI_PRO_MAX import mainAI

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
images_directory = os.path.join(os.getcwd(), "static/user_images")
app.mount("/static/user_images", StaticFiles(directory=images_directory), name="/static/user_images")

user_agreed = False
@app.get("/photobot")
async def read_root():
    if not user_agreed:
        return FileResponse("static/templates/about.html")
        # You can specify the HTML file you want to render here
    return FileResponse("static/templates/photobot.html")

@app.get("/")
async def read_root():
    if not user_agreed:
        return FileResponse("static/templates/about.html")
    # You can specify the HTML file you want to render here
    return FileResponse("static/templates/photobot.html")

@app.post("/agreement_accepted")
async def agreement_accepted():
    global user_agreed
    user_agreed = True
    return {"message": "User agreement accepted."}

@app.post("/request")
async def make_response(data: Request):
    body = await data.form()
    dialog = ""
    text = body['text'] if 'text' in body.keys() else None
    text = mainAI.AI_COMPIL(dialog, text)
    if 'image' in body.keys():
        image = body['image']
        ext = image.filename.split('.')[-1]
        image = await image.read()
        hashed_image = hashlib.sha256(image).hexdigest()
        filename = f'{str(hashed_image)}.{ext}'

        if filename not in os.listdir('static/user_images'):
            with open(f'static/user_images/{filename}', 'wb') as f:
                f.write(image)
    time.sleep(2)
    return Response(content=json.dumps({'text': text, 'image': None}), media_type="application/json")



@app.post("/get_image_hash")
async def get_image_hash(data: Request):
    body = await data.form()
    ext = body['image'].filename.split('.')[-1]
    image = await body['image'].read()
    hashed_image = hashlib.sha256(image).hexdigest()
    filename = f'{str(hashed_image)}.{ext}'
    return Response(content=json.dumps({'imageName': filename}), media_type="application/json")
