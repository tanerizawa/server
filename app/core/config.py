# app/core/config.py

import os
from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv

# Muat variabel dari file .env di lingkungan lokal
load_dotenv()

class Settings(BaseSettings):
    # Judul dan versi aplikasi
    PROJECT_NAME: str = "Dear Diary API"
    PROJECT_VERSION: str = "1.0.0"

    # --- Konfigurasi Database (Revisi Kritis) ---
    # DATABASE_URL sekarang wajib ada di lingkungan. Tidak ada lagi nilai
    # fallback ke SQLite untuk mencegah kesalahan koneksi di produksi.
    DATABASE_URL: str

    @field_validator("DATABASE_URL")
    def validate_db_url_is_postgres_in_prod(cls, v: str) -> str:
        """
        Validator ini memastikan bahwa di lingkungan produksi (seperti Render),
        aplikasi HARUS terhubung ke PostgreSQL. Jika tidak, aplikasi akan
        gagal memulai, yang lebih baik daripada berjalan dengan database yang salah.
        Render secara otomatis mengatur variabel 'RENDER' menjadi 'true'.
        """
        # Periksa apakah variabel RENDER ada untuk mendeteksi lingkungan produksi Render
        is_production = os.getenv("RENDER") == "true"

        if is_production and not v.startswith("postgresql"):
            raise ValueError(
                "Kesalahan Konfigurasi: Di lingkungan produksi, DATABASE_URL harus "
                "menunjuk ke database PostgreSQL."
            )
        return v
    # --- Akhir Revisi Kritis ---

    # Konfigurasi Redis untuk Celery
    # Gunakan variabel lingkungan untuk URL Redis, dengan fallback untuk pengembangan lokal
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

    # Konfigurasi model AI default
    GENERATOR_MODEL_NAME: str = os.getenv("GENERATOR_MODEL_NAME", "openrouter-default")
    PLANNER_MODEL_NAME: str = os.getenv("PLANNER_MODEL_NAME", "openrouter-default")

    # Identitas aplikasi untuk permintaan eksternal
    APP_NAME: str = os.getenv("APP_NAME", PROJECT_NAME)
    APP_SITE_URL: str = os.getenv("APP_SITE_URL", "http://localhost")

    class Config:
        case_sensitive = True

# Inisialisasi settings. Pydantic akan otomatis menjalankan validasi saat objek ini dibuat.
settings = Settings()