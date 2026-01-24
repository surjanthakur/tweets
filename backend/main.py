from fastapi import FastAPI
from db.db_connection import create_db_tables
from contextlib import asynccontextmanager
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PRODUCTION = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Creating database tables...")
        await create_db_tables()
        logger.info("Database created successfully 👍🏻.")
    except Exception as err:
        logger.error(f"db creation err: {err}")
        # If database creation fails, we stop the application from starting.
        raise

    # Yield the lifespan context manager
    yield
    logger.info("Shutting down...")


app = FastAPI(
    lifespan=lifespan,
    title="Tweet Analysis API",
    version="0.1",
    description="API for analyzing tweets using FastAPI",
    docs_url="/docs" if not PRODUCTION else None,
    redoc_url="/redoc" if not PRODUCTION else None,
    openapi_url="/openapi.json" if not PRODUCTION else None,
)
