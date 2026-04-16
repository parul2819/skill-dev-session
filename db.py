import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Validates environment variables at startup.
    If a variable is missing or of the wrong type, the app fails fast.
    """

    DB_DRIVER: str = "postgresql+asyncpg"
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = ""
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

    @property
    def database_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
logger = logging.getLogger(__name__)


# create_async_engine manages the pool of connections to the DB
engine = create_async_engine(
    settings.database_url,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=1800,
)

# async_sessionmaker is a factory for individual database sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """
    SQLAlchemy 2.0 Style Base class.
    Use this to inherit in your actual model files.
    """

    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to provide an AsyncSession to FastAPI routes.
    The async with block ensures the session is closed automatically
    even if the request crashes, preventing connection leaks.
    """
    async with AsyncSessionLocal() as session:
        yield session
