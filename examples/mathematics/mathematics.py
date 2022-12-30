from math import sqrt


def product(a: int, b: int) -> int:
    return a * b


def divide(a: float, b: float) -> float:
    return a / b


def negative(a: int) -> int:
    return a * -1


def square(a: int) -> int:
    return product(a, a)


def square_root(a: int) -> float:
    return sqrt(a)


def quadratic(a: int, b: int, c: int) -> tuple[float, float]:
    positive_solution = (
        negative(b) + square_root((square(b) - product(4, product(a, c))))
    ) / product(2, a)

    negative_solution = (
        negative(b) - square_root((square(b) - product(4, product(a, c))))
    ) / product(2, a)

    return (positive_solution, negative_solution)
