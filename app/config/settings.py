from pydantic_settings import BaseSettings, SettingsConfigDict

<<<<<<< HEAD
class Settings(BaseSettings):
    DATABASE_URL: str
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "restaurant_db"
=======

class Settings(BaseSettings):

    MONGO_URL: str
    DATABASE_NAME: str

    APP_NAME: str = "Restaurant Management System"
    DEBUG: bool = True

    # JWT Authentication settings
    JWT_SECRET_KEY: str = "supersecretjwtkeyforrestaurantmanagementsystem2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
>>>>>>> 6f39839 (your commit message)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()