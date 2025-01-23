import logging
import uuid
from fastapi import UploadFile
from botocore.exceptions import ClientError, BotoCoreError
from src.schemas.omamori import OmamoriInput, ShrineName, OmamoriSearchResults
from datetime import datetime
from src.db.s3 import upload_picture, delete_picture_by_object_name
from src.db.dbInstance import dynamodb
from src.custom_error import CustomException, ErrorCode, ErrorResponse
from src.utils.string_utils import (
    has_special_characters,
    has_script_tags,
    has_google_maps_url,
    has_japanese_characters,
    has_latin_characters
)
from src.utils.enum_types import UploadStatus, LocaleEnum
from src.utils.enum_types import PrefectureEnum, ProtectionTypeEnum


OMAMORI_TABLE = dynamodb.Table("omamori_data")


def search_omamori(
    prefecture: PrefectureEnum | None,
    protection: ProtectionTypeEnum | None
) -> list[OmamoriSearchResults]:
    try:
        omamori_search_result = {}

        if prefecture:
            expression_attributes_values = {
                ":prefecture_val": prefecture.value,
            }

            omamori_search_result = OMAMORI_TABLE.query(
                IndexName="prefecture_index",
                KeyConditionExpression="prefecture = :prefecture_val",
                ExpressionAttributeValues=expression_attributes_values,
            )

        if prefecture and protection:
            expression_attributes_values = {
                ":prefecture_val": prefecture.value,
                ":protection_val": protection.value
            }

            omamori_search_result = OMAMORI_TABLE.query(
                IndexName="prefecture_index",
                KeyConditionExpression="prefecture = :prefecture_val",
                FilterExpression="protection_type = :protection_val",
                ExpressionAttributeValues=expression_attributes_values,
            )

        return omamori_search_result["Items"]
    except (ClientError) as err:
        if ClientError:
            logging.error(
                "Couldn't retrieve omamori",
                "Here's why", err

            )

            raise CustomException(
                error={
                    "errors": [
                        {
                            "field": "search_omamori",
                            "error_code": ErrorCode.SERVER_ERROR.value,
                        }
                    ],
                    "has_error": True
                },
                status_code=500
            )


def create_omamori(omamori: OmamoriInput):
    try:
        validation_error = validate_create_omamori(omamori=omamori)

        if validation_error["has_error"]:
            raise CustomException(
                error=validation_error,
                status_code=402
            )

        db_entity = map_request_to_db_entity(omamori=omamori)

        OMAMORI_TABLE.put_item(Item=db_entity)
        # TO DO: on succesful creation log "omamori is succesful created"
        return db_entity
    except ClientError as err:
        logging.error(
            "Couldn't add omamori %s to table %s. Here's why: %s: %s",
            "omamori",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise CustomException(
            error={
                "errors": [
                    {
                        "field": "create_omamori",
                        "error_code": ErrorCode.SERVER_ERROR.value,
                    }
                ],
                "has_error": True
            },
            status_code=500
        )


def upload_omamori_picture(img_file: UploadFile, uuid: str):
    try:
        existing_omamori = OMAMORI_TABLE.get_item(
            Key={
                "uuid": uuid
            }
        )

        if "Item" not in existing_omamori:
            raise CustomException(
                error={
                    "errors": [
                        {
                            "field": "upload_omamori_picture",
                            "error_code": ErrorCode.OMAMORI_NOT_FOUND.value,
                        }
                    ],
                    "has_error": True
                },
                status_code=400
            )

        uploaded_picture_data: dict = upload_picture(img_file)

        update_expression = (
            "SET"
            "#upload_status = :upload_status,"
            "#picture_path = :picture_path,"
            "#updated_at = :updated_at"
        )

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

        updated_omamori = OMAMORI_TABLE.update_item(
            Key={
                "uuid": uuid
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return updated_omamori["Attributes"]
    except (ClientError, BotoCoreError, CustomException) as err:
        if CustomException:
            raise err

        if ClientError or BotoCoreError:
            deleted_picture = delete_picture_by_object_name(
                object_names=uploaded_picture_data)

            # TO DO: What to do if the picture was not deleted?

            logging.error("Couldn't updated omamori table",
                          "Here's why",
                          err,
                          "Deleted the picture in the S3 bucket as response",
                          deleted_picture)

            raise CustomException(
                error={
                    "errors": [
                        {
                            "field": "upload_omamori_picture",
                            "error_code": ErrorCode.SERVER_ERROR.value,
                        }
                    ],
                    "has_error": True
                },
                status_code=500
            )


def map_request_to_db_entity(omamori: OmamoriInput):
    current_date = datetime.now().isoformat()
    return {
        "uuid": str(uuid.uuid4()),
        "shrine_name":  [
            shrine.model_dump() for shrine in omamori.shrine_name
        ],
        "google_maps_link": omamori.google_maps_link,
        "prefecture": omamori.prefecture,
        "description": omamori.description,
        "protection_type": omamori.protection_type,
        "shrine_religion": omamori.shrine_religion,
        "upload_status": omamori.upload_status,
        "updated_at": current_date,
        "created_at": current_date
    }


def validate_create_omamori(omamori: OmamoriInput):
    validation_error = ErrorResponse(
        errors=[],
        has_error=False
    )

    validate_shrine_name(
        shrine_name=omamori.shrine_name,
        validation_error=validation_error
    )

    validate_google_url(
        google_url=omamori.google_maps_link,
        validation_error=validation_error
    )

    return validation_error


def validate_shrine_name(
        shrine_name: list[ShrineName],
        validation_error: ErrorResponse):

    if len(shrine_name) < 1:
        validation_error["has_error"] = True

    for name in shrine_name:
        if has_special_characters(name.name):
            validation_error["errors"].append({
                "field": "shrine_name",
                "error_code": ErrorCode.CONTAINS_INVALID_CHARACTER.value
            })
            validation_error["has_error"] = True

        if has_script_tags(name.name):
            validation_error["errors"].append({
                "field": "shrine_name",
                "error_code": ErrorCode.CONTAINS_INVALID_CHARACTER.value
            })
            validation_error["has_error"] = True

        if name.locale == LocaleEnum.en_US:
            if has_japanese_characters(name.name):
                validation_error["errors"].append({
                    "field": "shrine_name",
                    "error_code": ErrorCode.CONTAINS_JAPANESE_CHARACTER.value
                })
                validation_error["has_error"] = True

        if name.locale == LocaleEnum.ja_JP:
            if has_latin_characters(name.name):
                validation_error["errors"].append({
                    "field": "shrine_name",
                    "error_code": ErrorCode.CONTAINS_LATIN_CHARACTER.value
                })
                validation_error["has_error"] = True

    return validation_error


def validate_google_url(google_url: str, validation_error: ErrorResponse):
    # browser urls are max 2000 charcters
    if len(google_url) > 2000:
        validation_error["errors"].append({
            "field": "google_maps_link",
            "error_code": ErrorCode.INVALID_LENGTH_TOO_LONG.value
        })
        validation_error["has_error"] = True

    if not has_google_maps_url(google_url):
        validation_error["errors"].append({
            "field": "google_maps_link",
            "error_code": ErrorCode.INVALID_GOOGLE_MAP_URL.value
        })
        validation_error["has_error"] = True

    if has_script_tags(google_url):
        validation_error["errors"].append({
            "field": "google_maps_link",
            "error_code": ErrorCode.CONTAINS_INVALID_CHARACTER.value
        })
        validation_error["has_error"] = True

    return validation_error
