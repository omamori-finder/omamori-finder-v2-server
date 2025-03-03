from enum_types import ShrineReligionEnum, LocaleEnum, ProtectionTypeEnum, PrefectureEnum, UploadStatus
from service.omamori_service import create_omamori
omamori = [
    {
        "shrine_name": [
            {
                "name": "Meiji Jingu",
                "locale": LocaleEnum.en_US.value
            },
            {
                "name": "明治神宮",
                "locale": LocaleEnum.ja_JP.value
            }
        ],
        "google_maps_link": "https://maps.app.goo.gl/QJA696gaxJjQGKtp6",
        "prefecture": PrefectureEnum.Tokyo.value,
        "protection_type": ProtectionTypeEnum.good_luck.value,
        "shrine_religion": ShrineReligionEnum.Shinto.value,
        "description": ("Meiji Jingu is one of the Shinto shrines in Japan, with the vast land of the forest (70 ha.), located in the middle of the megacity, Tokyo."
                        "Once you step into this precinct, you will forget that you are in the hustle bustle city, and will find Japanese traditional scene amidst greenery nature."
                        "It was established in 1920, to commemorate the virtue of Emperor Meiji and Empress Shoken who took the initiative to make a foundation of modernized Japan."
                        ),
        "upload_status": UploadStatus.NOT_STARTED.value,
    }
]
