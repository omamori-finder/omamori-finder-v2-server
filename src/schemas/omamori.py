from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from enum import Enum
from src.enum_types import PrefectureEnum, ShrineReligionEnum, ProtectionTypeEnum


class OmamoriInput(BaseModel):
    shrine_name: str = Field(
        examples=['Meiji Jingu'], min_length=5, max_length=65)
    google_maps_link: str = Field(
        examples=['https://maps.app.goo.gl/RAAtiAsSBkA5X2UM6'], max_length=150, min_length=25)
    prefecture: PrefectureEnum
    description: str | None = Field(max_length=500)
    protection_type: ProtectionTypeEnum
    shrine_religion: ShrineReligionEnum
    photo_url: str = Field(
        examples=['url/something'], max_length=2000, min_length=1)


class OmamoriOut(OmamoriInput):
    uuid: UUID4
    updated_at: datetime
    created_at: datetime
