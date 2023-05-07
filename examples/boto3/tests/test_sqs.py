import fixtures
from example import sqs
from moto import mock_sqs

from sundew import test

test(sqs.send_message)(
    setup=[mock_sqs, fixtures.create_queue],
    kwargs={
        "queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/test-queue",
        "message_body": "{'test': 'body'}",
    },
    # This test returns a generated uuid. sundew doesn't currently support testing the
    # shape/property of a return statement
)
