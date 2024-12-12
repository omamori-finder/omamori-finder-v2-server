from pydantic import BaseModel, UUID4, Field
from datetime import datetime
from src.utils.enum_types import PrefectureEnum, ShrineReligionEnum, ProtectionTypeEnum, UploadStatus, LocaleEnum


class OmamoriPictureOut(BaseModel):
    object_key: str


class ShrineName(BaseModel):
    name: str = Field(examples=['Meiji Jingu'])
    locale: LocaleEnum


class OmamoriOut(BaseModel):
    uuid: UUID4
    shrine_name: list[ShrineName]
    updated_at: datetime
    created_at: datetime


class OmamoriInput(BaseModel):
    shrine_name: list[ShrineName]
    google_maps_link: str = Field(
        examples=['https://maps.app.goo.gl/RAAtiAsSBkA5X2UM6'])
    prefecture: PrefectureEnum
    protection_type: ProtectionTypeEnum
    shrine_religion: ShrineReligionEnum
    description: str | None = None
    upload_status: UploadStatus | None = UploadStatus.NOT_STARTED
