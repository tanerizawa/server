# app/core/config.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Tentukan path ke file .env. Ini membantu pydantic-settings menemukannya.
# Di Render, Secret Files akan ditempatkan di root direktori.
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')

class Settings(BaseSettings):
    # --- Konfigurasi pydantic-settings ---
    # Ini memberi tahu Pydantic untuk membaca dari file .env DAN dari environment variables.
    # Variabel lingkungan sistem (seperti yang di-inject oleh Render) akan menimpa nilai dari .env.
    model_config = SettingsConfigDict(
        env_file=dotenv_path,
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore' # Abaikan variabel ekstra yang tidak didefinisikan di model ini
    )

    # --- Variabel yang Dibutuhkan Aplikasi ---

    # Pengaturan Aplikasi Utama
    PROJECT_NAME: str = "Dear Diary API"
    PROJECT_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development" # Default ke development, akan ditimpa di produksi
    APP_NAME: str = "Dear Diary API"
    APP_SITE_URL: str = "http://localhost"

    # Database & Redis - WAJIB ADA
    DATABASE_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # Keamanan - WAJIB ADA
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 hari

    # Kredensial & Konfigurasi Layanan Eksternal
    OPENROUTER_API_KEY: str | None = None
    PLANNER_MODEL_NAME: str = "deepseek/deepseek-chat-v3-0324"
    GENERATOR_MODEL_NAME: str = "deepseek/deepseek-chat-v3-0324"
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    # Pengaturan Opsional (Contoh: CORS, Sentry)
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    SENTRY_DSN: str | None = None


# Buat satu instance settings untuk digunakan di seluruh aplikasi
settings = Settings()