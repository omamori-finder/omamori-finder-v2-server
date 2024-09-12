from fastapi import APIRouter
from src.schemas.omamori import OmamoriInput, Omamori
import src.service.omamori_service as service

router = APIRouter()


@router.get('/omamori')
async def get_omamori():
    return {'Here are some omamori 🎏'}


@router.post('/omamori')
async def create_omamori(omamori: OmamoriInput):
    new_omamori = await service.create_omamori(omamori=omamori)
    return new_omamori
