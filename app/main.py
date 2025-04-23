from fastapi import FastAPI
from app.routers import hackathons, auth, profile, role
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hahackathon.ru.tuna.am"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты
app.include_router(hackathons.router, prefix="/hackathons", tags=["Hackathons"])
app.include_router(auth.router, prefix="/auth", tags=["Authorization"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(role.router, prefix="/roles", tags=["Roles"])
