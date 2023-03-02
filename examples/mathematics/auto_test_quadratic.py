from sundew.test import test
from examples.mathematics.mathematics import product
from examples.mathematics.mathematics import divide
from examples.mathematics.mathematics import negative
from examples.mathematics.mathematics import square
from examples.mathematics.mathematics import square_root



test(negative)(
	kwargs={'a': -8},
	returns=8,
)

test(product)(
	kwargs={'a': -8, 'b': -8},
	returns=64,
)

test(product)(
	kwargs={'a': 4, 'b': 5},
	returns=20,
)

test(product)(
	kwargs={'a': 2, 'b': 1},
	returns=2,
)

test(product)(
	kwargs={'a': 1, 'b': 5},
	returns=5,
)

test(square)(
	kwargs={'a': -8},
	returns=64,
)

test(square_root)(
	kwargs={'a': 44},
	returns=6.6332495807108,
)

test(divide)(
	kwargs={'a': 1.3667504192892004, 'b': 2},
	returns=0.6833752096446002,
)

test(divide)(
	kwargs={'a': 14.6332495807108, 'b': 2},
	returns=7.3166247903554,
)

