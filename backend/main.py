from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from db.db_connection import create_db_tables
from fastapi.middleware.cors import CORSMiddleware
from router import userRouter


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

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    max_age=600,
)
app.include_router(router=userRouter.user_router, prefix="/api/v1.0")
