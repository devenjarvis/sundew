from collections.abc import Callable
from functools import partial
from typing import Any

import httpx


class AsyncTestClient(httpx.AsyncClient):
    def post_req(self, endpoint: str) -> Callable:
        new_func = partial(super().post, url=endpoint)
        new_func.__name__ = self.post_req.__name__
        new_func.__code__ = self.post.__code__
        new_func.__qualname__ = self.post_req.__qualname__
        new_func.__module__ = self.post_req.__module__
        return new_func


class TestClient(httpx.Client):
    def post_req(self, endpoint: str) -> Callable:
        new_func = partial(super().post, url=endpoint)
        new_func.__name__ = self.post_req.__name__
        new_func.__code__ = self.post.__code__
        new_func.__qualname__ = self.post_req.__qualname__
        new_func.__module__ = self.post_req.__module__
        return new_func


class TestResponse(httpx.Response):
    def __init__(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        # Call httpx.Respone __init__
        super().__init__(*args, **kwargs)
        # Unset headers if user didn't ask for it
        if not kwargs.get("headers", None):
            self.headers = None
        # Unset stream if user didn't ask for it
        if not kwargs.get("stream", None):
            self.stream = None

    def __eq__(self, other: httpx.Response) -> bool:
        for key, value in vars(self).items():
            if (
                not key.startswith("_")  # Ignore private attributes
                and value is not None  # Only check attributes set by user
                and value != getattr(other, key, None)  # Then check if equal
            ):
                return False

        return True
