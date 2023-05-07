# boto3 S3 Example
# Source: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs-examples.html
from typing import Optional

import boto3


def send_message(
    queue_url: str, message_body: str, message_attributes: Optional[dict] = None
) -> str:
    # Create SQS client
    sqs = boto3.client("sqs", region_name="us-east-1")

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes=message_attributes or {},
        MessageBody=message_body,
    )

    return response["MessageId"]


def recieve_message(queue_url: str) -> tuple[str, str]:
    # Create SQS client
    sqs = boto3.client("sqs")

    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=["SentTimestamp"],
        MaxNumberOfMessages=1,
        MessageAttributeNames=["All"],
        VisibilityTimeout=0,
        WaitTimeSeconds=0,
    )

    message = response["Messages"][0]
    receipt_handle = message["ReceiptHandle"]
    return (message, receipt_handle)


def delete_message(queue_url: str, receipt_handle: str) -> None:
    # Create SQS client
    sqs = boto3.client("sqs")

    # Delete received message from queue
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
