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
    returns=1,
)
