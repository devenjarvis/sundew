from sundew.test import test
from examples.strings.strings import concatenate
from examples.strings.strings import reverse



test(concatenate)(
	kwargs={'a': '456', 'b': '123'},
	returns='456123',
)

test(reverse)(
	kwargs={'a': '456123'},
	returns='321654',
)

