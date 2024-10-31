import logging
import uuid
from typing import TypedDict
from botocore.exceptions import ClientError
from src.schemas.omamori import OmamoriInput
from datetime import datetime
from src.db.s3 import upload_picture
from src.dbInstance import dynamodb
from src.custom_error import CustomException, ErrorCode
from src.utils.string_utils import has_special_characters, has_script_tags

# primary key is uuid

omamori_table = dynamodb.Table("omamori")


def create_omamori(omamori: OmamoriInput):
    try:
        validation_error = validate_create_omamori(omamori=omamori)

        if validation_error["has_error"]:
            raise CustomException(
                field="create_omamori", error_code=ErrorCode.VALIDATION_ERROR, status_code=402)

        db_entity = map_request_to_db_entity(omamori=omamori)

        omamori_table.put_item(Item=db_entity)
        # TO DO: on succesful creation log "omamori is succesful created"
        return db_entity
    except ClientError as err:
        logging.error(
            "Couldn't add omamori %s to table %s. Here's why: %s: %s",
            "omamori",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise CustomException(field="create_omamori",
                              error_code=ErrorCode.SERVER_ERROR,
                              status_code=500
                              )


def upload_omamori_picture(picture, uuid: str):
    try:
        uploaded_picture_data = upload_picture(picture)

        if uploaded_picture_data is None:
            raise Exception

        return uploaded_picture_data
    except Exception as err:
        print(err)
        raise CustomException(field="Upload_omamori_picture",
                              error_code=ErrorCode.SERVER_ERROR, status_code=500)
    # TO DO: Add service that handles the logic uploading the picture


def map_request_to_db_entity(omamori: OmamoriInput):
    current_date = datetime.now().isoformat()
    return {
        "uuid": str(uuid.uuid4()),
        "shrine_name": omamori.shrine_name,
        "google_maps_link": omamori.google_maps_link,
        "prefecture": omamori.prefecture,
        "description": omamori.description,
        "protection_type": omamori.protection_type,
        "shrine_religion": omamori.shrine_religion,
        "upload_status": omamori.upload_status,
        "updated_at": current_date,
        "created_at": current_date
    }


class ValidationError(TypedDict):
    has_error: bool


def validate_create_omamori(omamori: OmamoriInput):
    validation_error = ValidationError(has_error=False)

    validate_shrine_name(
        shrine_name=omamori.shrine_name, validation_error=validation_error)

    return validation_error


def validate_shrine_name(shrine_name: str, validation_error: ValidationError):

    if len(shrine_name.strip()) < 1:
        validation_error["has_error"] = True

    if has_special_characters(shrine_name):
        validation_error["has_error"] = True

    if has_script_tags(shrine_name):
        validation_error["has_error"] = True

    return validation_error
