import logging
import src.service.omamori_service as service
from fastapi import APIRouter, UploadFile, Form
from src.schemas.omamori import OmamoriOut, OmamoriInput, OmamoriPictureOut

router = APIRouter()


@router.get("/omamori")
async def get_omamori():
    return {"Here are some omamori 🎏"}


@router.post("/omamori")
async def create_omamori(omamori: OmamoriInput) -> OmamoriOut:
    logging.info(f"received omamori is {omamori}")
    new_omamori = service.create_omamori(omamori=omamori)
    return new_omamori


@router.post("/uploadpicture")
async def upload_omamori_picture(picture: UploadFile, uuid: str = Form(...)):
    uploaded_picture = service.upload_omamori_picture(
        picture=picture, uuid=uuid)
    return uploaded_picture
