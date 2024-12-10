import re


def has_special_characters(string_value: str) -> bool:
    regex_special_characters = r"[~`!#$%\^&*+={}()\-\[\]\\']+"
    contains_invalid_character = re.search(
        regex_special_characters, string_value)

    if contains_invalid_character != None:
        return True

    return False


def has_script_tags(string_value: str) -> bool:
    regex_script_tags = r"/<script.*?>.*?<\/script>/gi"
    contains_script_tags = re.search(regex_script_tags, string_value)

    if contains_script_tags != None:
        return True

    return False


def has_google_maps_url(string_value: str) -> bool:
    regex_google_maps_url = r"^(https?)://(maps\.app\.goo\.gl|www\.google\.com/maps)/"
    contains_google_maps_url = re.search(regex_google_maps_url, string_value)
    if contains_google_maps_url == None:
        return False
    return
