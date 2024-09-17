import boto3
import botocore.exceptions
from botocore.config import Config
import logging

logger = logging.getLogger(__name__)

# Some strange behavior here when using localhost as endpoint url to point to the docker container sometimes fails
# If this happens use the following url http://host.docker.internal:8000
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://host.docker.internal:8000",
    aws_access_key_id="testid",
    aws_secret_access_key="mysecret",
    region_name='localhost'
)


def create_table(table_name: str):
    try:
        omamori_table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    "AttributeName": "uuid",
                    "KeyType": "HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "uuid",
                    "AttributeType": "S"
                },
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        )

        print(table_name, "is",
              omamori_table)
    except botocore.exceptions.ClientError as err:
        print("Couldn't create table %s. Here's why: %s: %s",
              table_name,
              err.response["Error"]["Code"],
              err.response["Error"]["Message"]
              )
        raise


# create_table('omamori')
