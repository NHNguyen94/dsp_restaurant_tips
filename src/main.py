from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.api import router as v1_router
from src.database.models import create_tables


# https://fastapi.tiangolo.com/advanced/events/#startup-and-shutdown-together
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_tables()
        yield
    finally:
        pass


app = FastAPI(lifespan=lifespan)

app.include_router(v1_router)
