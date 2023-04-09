import inspect
from collections.abc import Callable
from typing import Any

from sundew.config import config
from sundew.types import FunctionTest


class FunctionSpy:
    def __init__(self, func: Callable) -> None:
        self.func = func
        self.calls: set[FunctionTest] = set()
        self.__name__ = func.__name__
        self.__qualname__ = func.__qualname__

    def __call__(
        self, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Any:  # noqa: ANN401
        generated_kwargs = inspect.getcallargs(self.func, *args, **kwargs)

        # Check cache
        if config.cache.contains(self.func, generated_kwargs):
            return config.cache.get_cached_value(self.func, generated_kwargs)

        answer = self.func(*args, **kwargs)
        function_test = FunctionTest(
            function=self.func,
            kwargs=generated_kwargs,
            returns=answer,
            cache=True,
        )
        self.calls.add(function_test)
        return answer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FunctionSpy):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (
            self.func.__code__.co_code == other.func.__code__.co_code
            and self.calls == other.calls
        )
