from pydantic import BaseModel, Field, UUID4
from typing import Annotated
from dataclasses import dataclass
from fastapi import Form, File
from datetime import datetime
from enum import Enum
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
    photo_url: Annotated[bytes, File()]
    description: str | None = Form(None)


class OmamoriInput(BaseModel):
    shrine_name: Annotated[str, Form(...)] = Field(
        examples=['Meiji Jingu'], min_length=5, max_length=65)
    google_maps_link: Annotated[str, Form(...)] = Field(
        examples=['https://maps.app.goo.gl/RAAtiAsSBkA5X2UM6'], max_length=150, min_length=25)
    prefecture: Annotated[PrefectureEnum, Form(...)]
    description: Annotated[str | None, Form(...)] = Field(max_length=500)
    protection_type: Annotated[ProtectionTypeEnum, Form(...)]
    shrine_religion: Annotated[ShrineReligionEnum, Form(...)]
    photo_url: Annotated[str, Form(...)] = Field(
        examples=['url/something'], max_length=2000, min_length=1)


class OmamoriOut(OmamoriInput):
    uuid: UUID4
    updated_at: datetime
    created_at: datetime
