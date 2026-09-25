from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.admin import create_admin
from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.core.config import settings

app = FastAPI()
app.add_middleware(CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SQLADMIN_SECRET_KEY)
app.include_router(health_router)
app.include_router(auth_router)
create_admin(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}