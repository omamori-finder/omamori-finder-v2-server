from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from enum import Enum
from src.enum_types import PrefectureEnum, ShrineReligionEnum, ProtectionTypeEnum


class OmamoriInput(BaseModel):
    shrine_name: str = Field(examples=['Meiji Jingu'])
    google_maps_link: str = Field(
        examples=['https://maps.app.goo.gl/RAAtiAsSBkA5X2UM6'])
    prefecture: PrefectureEnum
    description: str | None = None
    protection_type: ProtectionTypeEnum
    shrine_religion: ShrineReligionEnum
    photo_url: str = Field(examples=['url/something'])


class Omamori(BaseModel):
    uuid: UUID4
    shrine_name: str
    google_maps_link: str
    prefecture: PrefectureEnum
    description: str | None = None
    protection_type: ProtectionTypeEnum
    shrine_religion: ShrineReligionEnum
    photo_url: str
    updated_at: datetime
    created_at: datetime
