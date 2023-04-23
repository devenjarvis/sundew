# boto3 S3 Example
# Source: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import boto3


def create_table() -> None:
    # Get the service resource.
    dynamodb = boto3.resource("dynamodb")

    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName="users",
        KeySchema=[
            {"AttributeName": "username", "KeyType": "HASH"},
            {"AttributeName": "last_name", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "username", "AttributeType": "S"},
            {"AttributeName": "last_name", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    # Wait until the table exists.
    table.wait_until_exists()


def add_item() -> None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("users")
    table.put_item(
        Item={
            "username": "janedoe",
            "first_name": "Jane",
            "last_name": "Doe",
            "age": 25,
            "account_type": "standard_user",
        }
    )


def get_item() -> None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("users")
    response = table.get_item(Key={"username": "janedoe", "last_name": "Doe"})
    response["Item"]


def update_item() -> None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("users")
    table.update_item(
        Key={"username": "janedoe", "last_name": "Doe"},
        UpdateExpression="SET age = :val1",
        ExpressionAttributeValues={":val1": 26},
    )


def delete_item() -> None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("users")
    table.delete_item(Key={"username": "janedoe", "last_name": "Doe"})
