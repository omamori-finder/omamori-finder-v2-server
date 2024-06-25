from fastapi import FastAPI
from src.routes import omamori

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(omamori.router)
