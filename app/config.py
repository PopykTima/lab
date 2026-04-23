from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    
    # Цей рядок каже: "шукай значення у файлі .env"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()