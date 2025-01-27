from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from .models import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)

    yield

    pass
