import boto3
import logging
import uuid
from botocore.exceptions import ClientError, BotoCoreError
from src.custom_error import CustomException
from src.custom_error import ErrorCode

logger = logging.getLogger(__name__)


def upload_picture(file, bucket='omamori-finder-pictures-development') -> str:
    try:
        client = boto3.client('s3')
        object_name = f'media/{str(uuid.uuid4())}.jpg'
        client.upload_fileobj(file.file, bucket, object_name)
        return object_name
    except (ClientError, BotoCoreError) as err:
        logging.error("Was not able to upload the picture to S3 bucket",
                      "Here is why",
                      err)
        raise CustomException(field="upload_picture",
                              error_code=ErrorCode.SERVER_ERROR, status_code=500)


def delete_picture_by_object_name(object_name: str):
    client = boto3.client("s3")
    try:
        response = client.delete_object(
            Bucket="omamori-finder-pictures-development", Key=object_name)
        return response
    except ClientError as err:
        logging.error(err)
        return False
