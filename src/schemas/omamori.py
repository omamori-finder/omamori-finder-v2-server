from pydantic import BaseModel, UUID4, Field
from datetime import datetime
from src.utils.enum_types import PrefectureEnum, ShrineReligionEnum, ProtectionTypeEnum, UploadStatus

# Since we are using form data we are not able to use pydantic as input, that's why
# we needed to create a normal class


class OmamoriInput(BaseModel):
    shrine_name: str = Field(examples=['Meiji Jingu'])
    google_maps_link: str = Field(
        examples=['https://maps.app.goo.gl/RAAtiAsSBkA5X2UM6'])
    prefecture: PrefectureEnum
    protection_type: ProtectionTypeEnum
    shrine_religion: ShrineReligionEnum
    description: str | None = None
    upload_status: UploadStatus | None = UploadStatus.NOT_STARTED


class OmamoriOut(BaseModel):
    uuid: UUID4
    updated_at: datetime
    created_at: datetime


class OmamoriPictureOut(BaseModel):
    object_key: str
