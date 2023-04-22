# boto3 S3 Example
# Source: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs-examples.html
import boto3


def send_message() -> str:
    # Create SQS client
    sqs = boto3.client("sqs")

    queue_url = "SQS_QUEUE_URL"

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            "Title": {"DataType": "String", "StringValue": "The Whistler"},
            "Author": {"DataType": "String", "StringValue": "John Grisham"},
            "WeeksOn": {"DataType": "Number", "StringValue": "6"},
        },
        MessageBody=(
            "Information about current NY Times fiction bestseller for "
            "week of 12/11/2016."
        ),
    )

    return response["MessageId"]


def recieve_message() -> tuple[str, str]:
    # Create SQS client
    sqs = boto3.client("sqs")

    queue_url = "SQS_QUEUE_URL"

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
