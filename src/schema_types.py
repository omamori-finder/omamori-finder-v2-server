from pydantic import BaseModel, Field


class Omamori(BaseModel):
    shrine_name: str = Field(examples=['Meiji Jingu'])
    longitude: float = Field(examples=[35.675526])
    latitude: float = Field(examples=[139.6993])
    description: str = Field(
        examples=['Meiji Shrine is a Shinto shrine in Shibuya, Tokyo, that is dedicated to the deified spirits of Emperor Meiji and his wife, Empress Shōken.'])
    photo_url: str = Field(examples=['url/something'])
