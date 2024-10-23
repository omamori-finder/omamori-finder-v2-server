from pydantic import BaseModel, UUID4
from typing import Annotated
from dataclasses import dataclass
from fastapi import Form, UploadFile
from datetime import datetime
from src.enum_types import PrefectureEnum, ShrineReligionEnum, ProtectionTypeEnum

# Since we are using form data we are not able to use pydantic as input, that's why
# we needed to create a normal class


@dataclass
class OmamoriForm:
    shrine_name: Annotated[str, Form(...)]
    google_maps_link: Annotated[str, Form(...)]
    prefecture: Annotated[PrefectureEnum, Form(...)]
    protection_type: Annotated[ProtectionTypeEnum, Form(...)]
    shrine_religion: Annotated[ShrineReligionEnum, Form(...)]
    photo_url: UploadFile
    description: str | None = Form(None)


class OmamoriOut(BaseModel):
    uuid: UUID4
    updated_at: datetime
    created_at: datetime
