from fastapi import FastAPI
from app.routers import hackathons  # Убедись, что путь правильный

app = FastAPI()

# Подключаем роуты
app.include_router(hackathons.router, prefix="/hackathons", tags=["Hackathons"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
