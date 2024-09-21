import logging
from datetime import datetime
from http.client import HTTPException

from fastapi import FastAPI, Request, Response, BackgroundTasks, UploadFile, File
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import httpx
import hashlib
import os
import aiofiles
import uvicorn
from AI_PRO_MAX import mainAI, photogomo, imagekbqa
from hashlib import sha256

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
images_directory = os.path.join(os.getcwd(), "static/user_images")
app.mount("/user_images", StaticFiles(directory=images_directory), name="/user_images")
logging.basicConfig(filename='request_logs.log', level=logging.INFO, format='%(asctime)s - %(message)s')
tmp = "\\image:"


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


class RequestData(BaseModel):
    userMessages: List[Optional[str]] = []
    botMessages: List[Optional[str]] = []
    image: List[Optional[str]] = []
    flags: List[Optional[str]] = []


def extract_text(message: str, prefix: str) -> str:
    return message.split(prefix, 1)[-1].strip() if prefix in message else message.strip()


@app.post("/request")
async def make_response(request: Request, request_data: RequestData):
    client_host = request.client.host

    logging.info(f"Request received from IP: {client_host}, {request_data}")

    user_messages = [
        extract_text(msg, "text:") for msg in request_data.userMessages if msg
    ]
    bot_messages = [msg.strip() for msg in request_data.botMessages if msg]

    if request_data.image[0]:
        print(request_data.image)
        result_name = photogomo.main(f"static/user_images/{request_data.image[0]}")
        result = imagekbqa.main(result_name[1])
        text = mainAI.ai_main([result, result_name[0]], image_flag=True)
        logging.info(f"Request received from IP: {client_host}, Return {text}")
        return {"text": text, "image": None}

    for i in user_messages:
        if "\\image:" in i:
            result = photogomo.main(f"static/user_images/{i.replace(tmp, '')}")
            text = mainAI.ai_main(result, image_flag=True)
            logging.info(f"Request received from IP: {client_host}, Return {text}")
            return {"text": text, "image": None}

    else:
        data_for_ai = [user_messages[0]] if user_messages else []
        if bot_messages:
            data_for_ai.append(bot_messages[0])
        if len(user_messages) > 1:
            data_for_ai.append(user_messages[1])
        if 'regenerate' in request_data.flags:
            text = mainAI.ai_main(data_for_ai, regenerate_flag=True)
        else:
            text = mainAI.ai_main(data_for_ai)
        logging.info(f"Request received from IP: {client_host}, Return {text}")
        return {"text": text, "image": None}


async def save_image(image_data, file_path):
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(image_data)
        logging.info(f"Image saved to {file_path}")
    except Exception as e:
        logging.error(f"Failed to save image to {file_path}: {e}")
        raise HTTPException()


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


@app.get("/get_image_class")
async def get_image_class():
    pass


def test():
    with open("LOG.txt", 'w', encoding='utf-8') as f:
        f.write(mainAI.ai_main(["Чем мне удобрить свеклу"]))
        f.write(mainAI.ai_main(["Чем мне удобрить кукурузу?"]))
        f.write(mainAI.ai_main(["Чем мне удобрить карточку?"]))
        f.write(mainAI.ai_main(["Что такое биостим старт?"]))
        f.write(mainAI.ai_main(["Привет"]))
        f.write(mainAI.ai_main(["Кто ты?"]))
        f.write(mainAI.ai_main(["Чем ризоформ соя отличается от биостим рост?"]))
        f.write(mainAI.ai_main(["Как мне бороться с гниением картофеля?"]))
        f.write(mainAI.ai_main(["ОАОАОАОА"]))


if __name__ == "__main__":
    TEST = False
    if TEST:
        test()
    else:
        config = uvicorn.Config("main:app", reload=True, host="0.0.0.0", port=81, log_level="info")
        server = uvicorn.Server(config)
        server.run()
