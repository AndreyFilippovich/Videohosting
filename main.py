from api import video_router
from fastapi import FastAPI

app = FastAPI()


app.include_router(video_router)  # Подключаем эти url к нашему основному app
