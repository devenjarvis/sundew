# NOT COMPLETE
from examples.examples import fastapi_example
from sundew import test
from tests.examples import fixtures

test(fastapi_example.startup)(setup={fixtures.test_sqlite_db})
