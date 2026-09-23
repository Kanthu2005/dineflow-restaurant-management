from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "restaurant_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()