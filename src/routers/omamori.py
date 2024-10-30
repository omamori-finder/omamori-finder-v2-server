import logging
import src.service.omamori_service as service
from fastapi import APIRouter, Depends
from src.schemas.omamori import OmamoriOut, OmamoriForm

router = APIRouter()


@router.get("/omamori")
async def get_omamori():
    return {"Here are some omamori 🎏"}


@router.post("/upload")
async def upload_omamori_picture():
    return {"Omamori picture is uploaded"}


@router.post("/omamori")
async def create_omamori(omamori: OmamoriForm = Depends()) -> OmamoriOut:
    logging.info(f"received omamori is {omamori}")
    new_omamori = service.create_omamori(omamori=omamori)
    return new_omamori
