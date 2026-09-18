from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.admin import create_admin
from app.api.health import router as health_router
from app.core.config import settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SQLADMIN_SECRET_KEY)
app.include_router(health_router)
create_admin(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}