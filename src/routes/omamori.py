from fastapi import APIRouter
from src.schema_types import Omamori

router = APIRouter()


@router.get('/omamori')
async def get_omamori():
    return {'Omamori is created 🎏'}


@router.post('/omamori')
async def create_omamori(omamori: Omamori):
    print('Omamori data', omamori)
    return 'something'
