from pydantic_settings import BaseSettings
from sqlalchemy import create_engine


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str

    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@db:5432/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"


settings = Settings()

engine = create_engine(settings.database_url)