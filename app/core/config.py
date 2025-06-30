# app/core/config.py

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Muat variabel dari file .env di lingkungan lokal
load_dotenv()

class Settings(BaseSettings):
    # Judul dan versi aplikasi
    PROJECT_NAME: str = "Dear Diary API"
    PROJECT_VERSION: str = "1.0.0"

    # Konfigurasi Database
    # Gunakan variabel lingkungan untuk URL database, dengan fallback untuk pengembangan lokal
    # Contoh URL PostgreSQL: postgresql://user:password@host:port/dbname
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

    # Konfigurasi Redis untuk Celery
    # Gunakan variabel lingkungan untuk URL Redis
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # Kunci rahasia untuk JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret_key_default_should_be_changed")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 hari

    # Kredensial Spotify API
    SPOTIFY_CLIENT_ID: str | None = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET: str | None = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    # Kredensial OpenRouter AI
    OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")

    class Config:
        case_sensitive = True
        # Jika menggunakan Pydantic v1, gunakan:
        # env_file = ".env"
        # env_file_encoding = 'utf-8'

settings = Settings()

# Validasi sederhana saat startup
# Pastikan kunci penting ada di lingkungan produksi
# Anda dapat menambahkan validasi yang lebih ketat di sini
def check_production_settings():
    if not settings.DATABASE_URL.startswith("postgresql"):
        print("PERINGATAN: DATABASE_URL tidak disetel untuk PostgreSQL. Ini tidak ideal untuk produksi.")
    if settings.SECRET_KEY == "secret_key_default_should_be_changed":
        print("PERINGATAN: SECRET_KEY menggunakan nilai default. HARAP UBAH di lingkungan produksi.")