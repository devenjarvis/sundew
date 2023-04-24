import fixtures
from example import s3
from moto import mock_s3

from sundew import test

test(s3.upload_file)(
    setup=[mock_s3, fixtures.create_bucket, fixtures.test_file],
    kwargs={
        "file_name": "test-file",
        "bucket": "my-bucket",
        "object_name": "my-object",
    },
    returns=True,
)
