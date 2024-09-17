import boto3
import logging
import uuid
from fastapi import HTTPException
from botocore.exceptions import ClientError
from src.schemas.omamori import OmamoriInput, Omamori
from datetime import datetime
from src.dbInstance import dynamodb

# primary key is uuid

omamori_table = dynamodb.Table("omamori")


def create_omamori(omamori: OmamoriInput):
    try:
        omamori_uuid = str(uuid.uuid4())
        db_entity = map_request_to_db_entity(
            omamori=omamori, uuid=omamori_uuid)
        response = omamori_table.put_item(Item=db_entity)
        print('RESPONSE', response)
        return db_entity
    except ClientError as err:
        logging.error(
            "Couldn't add omamori %s to table %s. Here's why: %s: %s",
            'omamori',
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise HTTPException(status_code=400, detail="Could not create omamori")


def map_request_to_db_entity(omamori: OmamoriInput, uuid: str):
    current_date = datetime.now().isoformat()
    return {
        'uuid': uuid,
        'shrine_name': omamori.shrine_name,
        'google_maps_link': omamori.google_maps_link,
        'photo_url': omamori.photo_url,
        'description': omamori.description,
        'updated_at': current_date,
        'created_at': current_date
    }
