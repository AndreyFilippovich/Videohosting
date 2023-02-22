import shutil
from typing import List

from fastapi import APIRouter, File, Form, UploadFile
from models import User, Video
from schemas import GetVideo, Message, UploadVideo

video_router = APIRouter()


'''Позволяет загружать видео.
Сначала открываем файл, записываем его как "buffer.
Через shutil передаем, что мы будем записывать
'''


@video_router.post('/')
async def root(title: str = Form(...),
               description: str = Form(...),
               file: UploadFile = File(...)
               ):
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    user = await User.objects.first()
    return await Video.objects.create(file=file.filename,
                                      user=user,
                                      **info.dict()
                                      )


@video_router.get('/video/{video_pk}',
                  response_model=GetVideo,
                  responses={404: {'model': Message}}
                  )
async def get_video(video_pk: int):
    return await Video.objects.select_related('user').get(pk=video_pk)
