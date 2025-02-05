import logging
import src.service.omamori_service as service
from fastapi import APIRouter, UploadFile, Form
from src.schemas.omamori import OmamoriOut, OmamoriInput, OmamoriSearchResults
from src.utils.enum_types import PrefectureEnum, ProtectionTypeEnum

router = APIRouter()


@router.get("/omamori/")
async def search_omamori(
    prefecture: PrefectureEnum | None = None,
    protection: ProtectionTypeEnum | None = None,
    limit: int | None = 20,
    primary_start_key: str | None = None,
    sort_start_key: str | None = None
) -> OmamoriSearchResults:
    omamoris_by_prefecture = service.search_omamori(
        prefecture=prefecture,
        protection=protection,
        limit=limit,
        primary_start_key=primary_start_key,
        sort_start_key=sort_start_key
    )
    return omamoris_by_prefecture


@router.post("/omamori")
async def create_omamori(omamori: OmamoriInput) -> OmamoriOut:
    logging.info(f"received omamori is {omamori}")
    new_omamori = service.create_omamori(omamori=omamori)
    return new_omamori


@router.post("/uploadpicture")
async def upload_omamori_picture(picture: UploadFile, uuid: str = Form(...)):
    uploaded_picture = service.upload_omamori_picture(
        img_file=picture, uuid=uuid)
    return uploaded_picture
