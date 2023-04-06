from examples.examples import fastapi_example
from sundew import AsyncTestClient, TestResponse, test

client = AsyncTestClient(app=fastapi_example.app, base_url="http://testserver")


test(fastapi_example.read_notes, client.post_req("/notes/"))(
    kwargs={
        "json": {"text": "test2", "completed": False},
    },
    returns=TestResponse(
        status_code=200,
        json={"id": 1, "text": "test2", "completed": False},
        headers={"content-length": "42", "content-type": "application/json"},
    ),
)
