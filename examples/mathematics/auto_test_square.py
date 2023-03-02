from sundew.test import test
from examples.mathematics.mathematics import product



test(product)(
	kwargs={'a': -8, 'b': -8},
	returns=64,
)

