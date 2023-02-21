import shutil
from typing import List

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


'''Позволяет загружать видео.
Сначала открываем файл, записываем его как "buffer.
Через shutil передаем, что мы будем записывать
'''


@app.post('/')
async def root(file: UploadFile = File(...)):
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {'file_name': file.filename}


'''Позволяет загружать фотографии.'''


@app.post('/img')
async def upload_image(files: List[UploadFile] = File(...)):
    for img in files:
        with open(f'{img.filename}', "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
    return {'file_name': "Good"}
