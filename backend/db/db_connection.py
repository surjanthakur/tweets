from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker

from sqlmodel.ext.asyncio.session import AsyncSession
import logging
from typing import AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Database configuration using Pydantic BaseSettings
class Settings(BaseSettings):
    db_url: str
    db_echo: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="allow",
    )


# Initialize settings from environment variables
env_settings = Settings()

# Create asynchronous database engine
engine: AsyncEngine = create_async_engine(
    env_settings.db_url,
    echo=env_settings.db_echo,
    pool_pre_ping=True,
)

#  Create asynchronous session maker
session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# Dependency to get an async database session/transaction.
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker().begin() as session:
        try:
            yield session
        except SQLAlchemyError as err:
            logger.error(f"database current session error: {err}")
            await session.rollback()
            raise
        except Exception as err:
            logger.error(f"error while get session: {err}")
            await session.rollback()
            raise
        finally:
            await session.close()


# Function to create database tables.
async def create_db_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except SQLAlchemyError as err:
        logger.error(f"database table creation error: {err}")
        raise
