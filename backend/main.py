from fastapi import FastAPI
from router.profile import profile_router
from contextlib import asynccontextmanager
import logging
from db.db_connection import create_db_tables


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
    docs_url=None if PRODUCTION else "/docs",
    redoc_url=None if PRODUCTION else "/redoc",
    openapi_url=None if PRODUCTION else "/openapi.json",
)


app.include_router(router=profile_router)
