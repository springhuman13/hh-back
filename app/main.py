from fastapi import FastAPI
from app.routers import hackathons
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Подключаем роуты
app.include_router(hackathons.router, prefix="/hackathons", tags=["Hackathons"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Вы можете ограничить доступ конкретными доменами
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)