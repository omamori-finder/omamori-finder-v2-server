import boto3
import logging
import uuid
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def upload_picture(file, bucket='omamori-finder-pictures'):
    try:
        client = boto3.client('s3')
        object_name = f'media/{str(uuid.uuid4())}.jpg'
        client.upload_fileobj(file.file, bucket, object_name)
    # TO DO: Raise custom error here
    except ClientError as err:
        logging.error("Was not able to upload the picture to S3 bucket",
                      "Here is why",
                      err)
        return False
    return object_name


def delete_picture_by_object_name(object_name: str):
    client = boto3.client("s3")
    try:
        response = client.delete_object(
            Bucket="omamori-finder-pictures", Key=object_name)
        return response
    except ClientError as err:
        logging.error(err)
        return False
