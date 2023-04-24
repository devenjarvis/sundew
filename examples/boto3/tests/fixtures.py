import logging
from contextlib import contextmanager
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


@contextmanager
def test_file() -> None:
    try:
        temp_file = Path("./test-file")
        temp_file.touch()
        yield
    finally:
        temp_file.unlink()


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
