def concatenate(a: str, b: str) -> str:
    return a + b


def reverse(a: str) -> str:
    return a[::-1]


def make_silly(a: str, b: str) -> str:
    return reverse(concatenate(b, a))


def print_string(a: str):
    print(a)
