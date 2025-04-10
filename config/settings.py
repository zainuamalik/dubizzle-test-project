from enum import Enum
from pydantic_settings import BaseSettings


class OrderStatus(str, Enum):
    pending = 'pending'
    cancelled = 'cancelled'
    completed = 'completed'


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int


    class Config:
        env_file = ".env"


settings = Settings()