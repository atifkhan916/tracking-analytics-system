from pydantic_settings import BaseSettings
from typing import Optional
import json

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tracking Analytics API"
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: Optional[str] = None
    DB_PASSWORD_ARN: Optional[str] = None
    ENVIRONMENT: Optional[str] = "development"
    REGION: Optional[str] = None


    @property
    def DATABASE_URL(self) -> str:
        """
        Construct database URL using resolved password
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()