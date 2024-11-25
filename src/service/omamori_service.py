import logging
import uuid
from typing import TypedDict
from botocore.exceptions import ClientError, BotoCoreError
from src.schemas.omamori import OmamoriInput
from datetime import datetime
from src.db.s3 import upload_picture, delete_picture_by_object_name
from src.dbInstance import dynamodb
from src.custom_error import CustomException, ErrorCode
from src.utils.string_utils import has_special_characters, has_script_tags
from src.enum_types import UploadStatus

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

        update_expression = "SET #upload_status = :upload_status, #picture_path = :picture_path, #updated_at = :updated_at"

        expression_attribute_names = {
            "#upload_status": "upload_status",
            "#picture_path": "picture_path",
            "#updated_at": "updated_at"
        }

        expression_attribute_values = {
            ":upload_status": UploadStatus.COMPLETED,
            ":picture_path": uploaded_picture_data,
            ":updated_at": datetime.now().isoformat()
        }

        updated_omamori = omamori_table.update_item(
            Key={
                "uuid": uuid
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return updated_omamori["Attributes"]
    except (ClientError, BotoCoreError) as err:

        if ClientError or BotoCoreError:
            deleted_picture = delete_picture_by_object_name(
                object_name=uploaded_picture_data)

            # TO DO: What to do if the picture was not deleted?

            logging.error("Couldn't updated omamori table",
                          "Here's why",
                          err,
                          "Deleted the picture in the S3 bucket as response",
                          deleted_picture)

        raise CustomException(field="Upload_omamori_picture",
                              error_code=ErrorCode.SERVER_ERROR, status_code=500)


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
