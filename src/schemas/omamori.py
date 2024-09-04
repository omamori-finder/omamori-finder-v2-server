from pydantic import BaseModel, Field


class Omamori(BaseModel):
    shrine_name: str = Field(examples=['Meiji Jingu'])
    google_maps_link: str = Field(
        examples=['https://maps.app.goo.gl/RAAtiAsSBkA5X2UM6'])
    description: str = Field(
        examples=['Meiji Shrine is a Shinto shrine in Shibuya, Tokyo, that is dedicated to the deified spirits of Emperor Meiji and his wife, Empress Shōken.'])
    photo_url: str = Field(examples=['url/something'])
