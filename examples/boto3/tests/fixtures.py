import logging
from contextlib import contextmanager
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from example import s3


@contextmanager
def test_file() -> None:
    try:
        temp_file = Path("./test-file")
        temp_file.touch()
        yield
    finally:
        temp_file.unlink()


@contextmanager
def cleanup_test_file_2() -> None:
    yield
    Path("./test-file-2.txt").unlink()


@contextmanager
def create_bucket() -> None:
    try:
        s3_resource = boto3.resource("s3", region_name="us-east-1")
        s3_resource.create_bucket(Bucket="my-bucket")
    except ClientError:
        logging.exception("boto3 client error")
    else:
        yield
    finally:
        bucket = s3_resource.Bucket("my-bucket")
        bucket.objects.all().delete()
        bucket.delete()


@contextmanager
def create_queue() -> None:
    try:
        sqs = boto3.client("sqs", region_name="us-east-1")

        # Create a SQS queue
        response = sqs.create_queue(QueueName="test-queue")
    except ClientError:
        logging.exception("boto3 client error")
    else:
        yield
    finally:
        queue_url = response["QueueUrl"]
        sqs.delete_queue(QueueUrl=queue_url)


@contextmanager
def upload_object() -> None:
    s3.upload_file(file_name="test-file", bucket="my-bucket", object_name="my-object")
    yield
