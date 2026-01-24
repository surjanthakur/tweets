from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
import logging
from typing import AsyncGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    db_url: str
    db_echo: bool = False

    env_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


env_settings = Settings()

engine: AsyncEngine = create_async_engine(
    env_settings.db_url,
    echo=env_settings.env_config,
    pool_pre_ping=True,
)

session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)
