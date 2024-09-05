import boto3
import botocore.exceptions
import logging

logger = logging.getLogger(__name__)

dynamodb = boto3.client("dynamodb", endpoint_url='http://localhost:8000')


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
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        logger.error(f"{table_name} is {
                     omamori_table['TableDescription']['TableStatus']}"
                     )
    except botocore.exceptions.ClientError as err:
        logger.error("Couldn't create table %s. Here's why: %s: %s",
                     table_name,
                     err.response["Error"]["Code"],
                     err.response["Error"]["Message"]
                     )
        raise


create_table("omamori")
