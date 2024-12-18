import boto3
import logging
import uuid
from io import BytesIO
from PIL import Image
from fastapi import UploadFile
from botocore.exceptions import ClientError, BotoCoreError
from src.custom_error import ErrorCode, CustomException

logger = logging.getLogger(__name__)

BUCKET_NAME = "omamori-finder-pictures-development"


def resize_image(image, size: tuple):
    try:
        with Image.open(image) as im:
            im.thumbnail(size)
            buffer = BytesIO()
            im.save(buffer, "JPEG")
            buffer.seek(0)
            return buffer
    except OSError:
        print("cannot create thumbnail for", image)


def upload_picture(img_file: UploadFile) -> str:
    try:
        image_uuid = str(uuid.uuid4())

        image_sizes = {
            "desktop_size": (1080, 1080),
            "mobile_size": (640, 640),
            "mobile_small_size": (300, 300)
        }

        client = boto3.client('s3')

        image_paths = {}

        for type_size, size in image_sizes.items():

            object_name = f'images/{image_uuid}/{type_size}.jpg'

            resized_image = resize_image(image=img_file.file, size=size)

            client.upload_fileobj(resized_image, BUCKET_NAME, object_name)

            image_paths[type_size] = object_name

        return image_paths
    except (ClientError, BotoCoreError) as err:
        logging.error("Was not able to upload the picture to S3 bucket",
                      "Here is why",
                      err)
        raise CustomException(
            error={
                "errors": [
                    {
                        "field": "upload_picture",
                        "error_code": ErrorCode.SERVER_ERROR.value,
                    }
                ],
                "has_error": True
            },
            status_code=500
        )


def delete_picture_by_object_name(object_names: dict):
    client = boto3.client("s3")
    try:
        images_to_delete = [{'Key': path} for path in object_names.values()]

        response = client.delete_objects(
            Bucket=BUCKET_NAME,
            Delete={'Objects': images_to_delete}
        )

        return response
    except ClientError as err:
        logging.error(err)
        return False
