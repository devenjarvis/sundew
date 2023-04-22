# boto3 S3 Example
# Source: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html

import logging
import os

import boto3
from botocore.exceptions import ClientError


def upload_file(file_name: str, bucket: str, object_name: str | None = None) -> None:
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(bucket_name, object_name, file_name):
    s3 = boto3.client("s3")
    with open(file_name, "wb") as f:
        s3.download_fileobj(bucket_name, object_name, f)
