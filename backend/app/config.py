from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./crm.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "change_this_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    OPENAI_API_KEY: str | None = None
    ALLOWED_ORIGINS: str = "*"

    class Config:
        env_file = ".env"


settings = Settings()
