from fastapi import FastAPI
from src.routers import omamori
from contextlib import asynccontextmanager
from src.dbInstance import create_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table("omamori")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(omamori.router)
