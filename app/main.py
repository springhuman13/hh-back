from fastapi import FastAPI
from app.routers import hackathons
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Подключаем роуты
app.include_router(hackathons.router, prefix="/hackathons", tags=["Hackathons"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)