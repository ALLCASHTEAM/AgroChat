from fastapi import FastAPI, Request, Response, BackgroundTasks, UploadFile, File
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import hashlib
import os
import aiofiles
import uvicorn
from AI_PRO_MAX import mainAI, photogomo
from hashlib import sha256

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
images_directory = os.path.join(os.getcwd(), "static/user_images")
app.mount("/static/user_images", StaticFiles(directory=images_directory), name="/static/user_images")


@app.get("/")
async def read_root():
    # You can specify the HTML file you want to render here
    return FileResponse("static/index.html")


class RequestData(BaseModel):
    userMessages: List[Optional[str]]
    botMessages: List[Optional[str]]
    image: List[Optional[str]]


@app.post("/request")
async def make_response(request_data: RequestData):
    user_messages = [msg.split("text:", 1)[-1] for msg in request_data.userMessages if msg]
    bot_messages = [msg for msg in request_data.botMessages if msg]

    if request_data.image:
        print(request_data.image)
        result = photogomo.main(f"static/user_images/{request_data.image[0]}")
        text = mainAI.AI_COMPIL(result, imageFlag=True)
        return {"text": text, "image": None}
    # request_data.image - хеш каритинки ну и плюс название файла
    else:
    # Формируем data_for_ai, добавляя первое сообщение пользователя и бота, а также второе сообщение пользователя, если оно есть
        data_for_ai = [user_messages[0]] if user_messages else []
        if bot_messages:
            data_for_ai.append(bot_messages[0])
        if len(user_messages) > 1:
            data_for_ai.append(user_messages[1])
        text = mainAI.AI_COMPIL(data_for_ai)
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

    if filename not in os.listdir('static/user_images'):
        await save_image(image, f'static/user_images/{filename}')
    return Response(content=json.dumps({'imageName': filename}), media_type="application/json")


if __name__ == "__main__":
    config = uvicorn.Config("main:app", reload=True, host="0.0.0.0", port=81, log_level="info")
    server = uvicorn.Server(config)
    server.run()
