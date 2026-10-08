from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.admin import create_admin
from app.api.activity_types import router as activity_types_router
from app.api.auth import router as auth_router
from app.api.calendar import router as calendar_router
from app.api.goals import router as goals_router
from app.api.health import router as health_router
from app.api.plans import router as plans_router
from app.api.sessions import router as sessions_router
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
app.include_router(sessions_router)
app.include_router(plans_router)
app.include_router(activity_types_router)
app.include_router(goals_router)
app.include_router(calendar_router)
create_admin(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}