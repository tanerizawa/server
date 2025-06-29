import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./test.db")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # API keys and model configuration for the AI chat features
    OPENROUTER_API_KEY: str | None = None
    PLANNER_MODEL_NAME: str = "deepseek/deepseek-chat-v3-0324"
    GENERATOR_MODEL_NAME: str = "deepseek/deepseek-chat-v3-0324"
    APP_SITE_URL: str = "https://bizmark.id"
    APP_NAME: str = "Dear Diary"
    SPOTIFY_CLIENT_ID: str | None = None
    SPOTIFY_CLIENT_SECRET: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
