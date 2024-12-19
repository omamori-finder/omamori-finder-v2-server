import boto3
import logging

logger = logging.getLogger(__name__)


# Some strange behavior here when using localhost as endpoint url to point
# to the docker container sometimes fails this
# happens use the following url http://host.docker.internal:8000
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://host.docker.internal:8000",
    aws_access_key_id="X",
    aws_secret_access_key="X",
    region_name="localhost"
)
