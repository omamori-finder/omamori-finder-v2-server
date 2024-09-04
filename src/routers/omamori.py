from fastapi import APIRouter
from src.schemas.omamori import Omamori

router = APIRouter()


@router.get('/omamori')
async def get_omamori():
    return {'Here are some omamori 🎏'}


@router.post('/omamori')
async def create_omamori(omamori: Omamori):
    print('Omamori data', omamori)
    return {'Omamori is created 🎏'}
