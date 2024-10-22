import boto3
import logging
import uuid
import os
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# s3 = boto3.resource('s3')

# bucket = s3.Bucket('omamori-finder-pictures')
# print(bucket)


def upload_file(file, bucket='omamori-finder-pictures'):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    client = boto3.client('s3')
    # content = file.file.read()
    # file.file.seek(0)
    object_name = f'media/{str(uuid.uuid4())}.jpg'
    # If S3 object_name was not specified, use file_name
    # object_name = os.path.basename(file_name)
    try:
        response = client.upload_fileobj(file.file, bucket, object_name)
        print("RESPONSE S3 BUCKET", response)
    except ClientError as e:
        logging.error(e)
        return False
    return object_name
