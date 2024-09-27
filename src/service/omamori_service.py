import logging
import uuid
from fastapi import HTTPException
from botocore.exceptions import ClientError
from src.schemas.omamori import OmamoriInput
from datetime import datetime
from src.dbInstance import dynamodb
from src.result import ErrorCode

# primary key is uuid

omamori_table = dynamodb.Table("omamori")


def create_omamori(omamori: OmamoriInput):
    try:
        omamori_uuid = str(uuid.uuid4())
        db_entity = map_request_to_db_entity(
            omamori=omamori, uuid=omamori_uuid)
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
        raise HTTPException(status_code=500, detail="Internal server error")


def map_request_to_db_entity(omamori: OmamoriInput, uuid: str):
    current_date = datetime.now().isoformat()
    return {
        "uuid": uuid,
        "shrine_name": omamori.shrine_name,
        "google_maps_link": omamori.google_maps_link,
        "prefecture": omamori.prefecture,
        "description": omamori.description,
        "protection_type": omamori.protection_type,
        "shrine_religion": omamori.shrine_religion,
        "photo_url": omamori.photo_url,
        "updated_at": current_date,
        "created_at": current_date
    }
