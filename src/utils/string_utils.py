import re


def has_special_characters(string_value: str) -> bool:
    regex_special_characters = r"[~`?!#$%\^&*+={}()\-\[\]\\']+"
    contains_invalid_character = re.search(
        regex_special_characters, string_value)

    if contains_invalid_character is not None:
        return True

    return False


def has_script_tags(string_value: str) -> bool:
    regex_script_tags = r"<script\b.*?>.*?</script>"
    contains_script_tags = re.search(
        regex_script_tags, string_value, re.IGNORECASE)

    if contains_script_tags is not None:
        return True

    return False


def has_google_maps_url(string_value: str) -> bool:
    regex_google_maps_url = r"""
        ^(https?):\/\/(maps\.app\.goo\.gl\b|(www\.)?google\.com/maps)/
    """
    contains_google_maps_url = re.search(
        regex_google_maps_url, string_value, re.VERBOSE)

    if contains_google_maps_url is None:
        return False

    return True


def has_japanese_characters(string_value: str) -> bool:
    regex_japanese_characters = r"[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf]+"
    contains_japanese_characters = re.search(
        regex_japanese_characters, string_value)

    if contains_japanese_characters is None:
        return False

    return True


def has_latin_characters(string_value: str) -> bool:
    regex_latin_characters = r"[a-zA-Z]+"
    contains_latin_characters = re.search(regex_latin_characters, string_value)

    if contains_latin_characters is None:
        return False

    return True
