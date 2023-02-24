from starlette.responses import StreamingResponse
from starlette.templating import Jinja2Templates
from typing import List

from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from models import User, Video
from schemas import GetVideo, Message, UploadVideo
from services import write_video, save_video

video_router = APIRouter()
templates = Jinja2Templates(directory="templates")


'''Загружаем видео и оно сохраняется.
Загружаем только файлы mp4.
Если это нужный файл, то мы его обрабатывает,
а если нет, то выдаем ошибку 418
'''


@video_router.post('/')
async def create_video(
    back_tasks: BackgroundTasks,
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...)
):
    user = await User.objects.first()
    return await save_video(user,
                            file,
                            title,
                            description,
                            back_tasks
                            )


@video_router.get('/video/{video_pk}', responses={404: {'model': Message}})
async def get_video(video_pk: int):
    file = await Video.objects.select_related('user').get(pk=video_pk)
    file_like = open(file.dict().get('file'), mode='rb')
    return StreamingResponse(file_like, media_type='video/mp4')
