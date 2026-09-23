import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "restaurant_db"
    PORT: int = int(os.getenv("PORT", "8001"))


settings = Settings()
