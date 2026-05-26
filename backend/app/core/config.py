from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str
    PROJECT_NAME: str = "Quiz dos Professores"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
