import boto3
import logging
import uuid
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def upload_picture(file, bucket='omamori-finder-pictures'):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    client = boto3.client('s3')
    object_name = f'media/{str(uuid.uuid4())}.jpg'
    try:
        response = client.upload_fileobj(file.file, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return object_name
