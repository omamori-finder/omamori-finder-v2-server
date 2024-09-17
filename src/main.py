from fastapi import FastAPI
from src.routers import omamori
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(omamori.router)
