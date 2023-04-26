import os

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

test(s3.download_file)(
    setup=[
        mock_s3,
        fixtures.create_bucket,
        fixtures.test_file,
        fixtures.upload_object,
        fixtures.cleanup_test_file_2,
    ],
    kwargs={
        "bucket_name": "my-bucket",
        "object_name": "my-object",
        "file_name": "test-file-2.txt",
    },
    side_effects={lambda _: os.path.isfile(_.file_name)},  # noqa: PTH113
)
