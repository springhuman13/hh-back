from fastapi import FastAPI
from app.routers import hackathons, auth, profile, role, city, team, application, notification
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
app.include_router(city.router, prefix="/cities", tags=["Cities"])
app.include_router(team.router, prefix="/team", tags=["Team"])
app.include_router(application.router, prefix="/application", tags=["Application"])
app.include_router(notification.router, prefix="/notification", tags=["Notification"])
