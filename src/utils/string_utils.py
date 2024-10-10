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
