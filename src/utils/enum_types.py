from enum import Enum


class LocaleEnum(str, Enum):
    en_US = "en_US"
    ja_JP = "ja_JP"


class UploadStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    UPLOADING = "UPLOADING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ShrineReligionEnum(str, Enum):
    Buddhism = "Buddhism"
    Shinto = "Shinto"


class ProtectionTypeEnum(str, Enum):
    happiness = "happiness"
    good_luck = "good luck"
    traffic = "traffic"
    love = "love"
    marriage = "marriage"
    health = "health"
    success = "success"
    family = "family"
    pregnancy = "pregnancy"
    safe_birth = "safe birth"


class PrefectureEnum(str, Enum):
    Hokkaido = "Hokkaido"
    Aomori = "Aomori"
    Iwate = "Iwate"
    Miyagi = "Miyagi"
    Akita = "Akita"
    Yamagata = "Yamagata"
    Fukushima = "Fukushima"
    Ibaraki = "Ibaraki"
    Tochigi = "Tochigi"
    Gumma = "Gumma"
    Saitama = "Saitama"
    Chiba = "Chiba"
    Tokyo = "Tokyo"
    Kanagawa = "Kanagawa"
    Niigata = "Niigata"
    Toyama = "Toyama"
    Ishikawa = "Ishikawa"
    Fukui = "Fukui"
    Yamanashi = "Yamanashi"
    Nagano = "Nagano"
    Gifu = "Gifu"
    Shizuoka = "Shizuoka"
    Aichi = "Aichi"
    Mie = "Mie"
    Shiga = "Shiga"
    Kyoto = "Kyoto"
    Osaka = "Osaka"
    Hyogo = "Hyogo"
    Nara = "Nara"
    Wakayama = "Wakayama"
    Tottori = "Tottori"
    Shimane = "Shimane"
    Okayama = "Okayama"
    Hiroshima = "Hiroshima"
    Yamaguchi = "Yamaguchi"
    Tokushima = "Tokushima"
    Kagawa = "Kagawa"
    Ehime = "Ehime"
    Kochi = "Kochi"
    Fukuoka = "Fukuoka"
    Saga = "Saga"
    Nagasaki = "Nagasaki"
    Kumamoto = "Kumamoto"
    Oita = "Oita"
    Miyazaki = "Miyazaki"
    Kagoshima = "Kagoshima"
    Okinawa = "Okinawa"
