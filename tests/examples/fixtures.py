from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import databases


@contextmanager
def test_sqlite_db() -> Iterator:
    try:
        # Create temporary sqlite db
        new_db_file = Path("./test_fastapi_example.db")
        new_db_file.touch()
        test_database_url = "sqlite:///./test_fastapi_example.db"
        database = databases.Database(test_database_url, force_rollback=True)

        yield database
    finally:
        # delete temporary db
        new_db_file.unlink()
