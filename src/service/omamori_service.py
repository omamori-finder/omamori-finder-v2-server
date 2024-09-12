import boto3
import uuid
from fastapi import HTTPException
from botocore.exceptions import ClientError
from src.schemas.omamori import OmamoriInput, Omamori
from datetime import datetime
from src.dbInstance import dynamodb

# primary key is uuid


def create_omamori(omamori: OmamoriInput):
    try:
        db_entity = map_request_to_db_entity(omamori=omamori)
        response = dynamodb.put_item(TableName='omamori', Item=db_entity)
        print('response of db', response)
        return db_entity
    except ClientError as err:
        print(
            "Couldn't add omamori %s to table %s. Here's why: %s: %s",
            'omamori',
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise HTTPException(status_code=400, detail="Could not create omamori")


def map_request_to_db_entity(omamori: OmamoriInput):
    return {
        'uuid': {"S": str(uuid.uuid4())},
        'shrine_name': {"S":  omamori.shrine_name},
        'google_maps_link': {"S": omamori.google_maps_link},
        'photo_url': {"S": omamori.photo_url},
        'description': {"S": omamori.description},
        'updated_at': {"S": datetime.now().isoformat()},
        'created_at': {"S": datetime.now().isoformat()}
    }
