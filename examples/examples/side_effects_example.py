def concatenate(a: str, b: str) -> str:
    return a + b


def reverse(a: str) -> str:
    return a[::-1]


def make_silly(a: str, b: str) -> str:
    return reverse(concatenate(b, a))


def print_string(a: str) -> None:
    print(a)  # noqa: T201


def print_hello(name: str) -> None:
    print(f"Hello, {name}")  # noqa: T201
