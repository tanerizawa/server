# backend/app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.api import api_router
import os
from alembic import command
from alembic.config import Config

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run database migrations on startup."""
    print("Running database migrations...")
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    command.upgrade(alembic_cfg, "head")
    print("Migrations complete.")
    yield
    # Kode untuk dijalankan saat shutdown bisa ditambahkan di sini

app = FastAPI(title="Dear Diary API", lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Dear Diary API"}
