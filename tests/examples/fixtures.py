from collections.abc import Iterator
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path

import databases
from httpx import AsyncClient

from examples.examples import fastapi_example


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


@asynccontextmanager
async def test_client() -> Iterator:
    async with AsyncClient(
        app=fastapi_example.app, base_url="http://test"
    ) as test_client:
        yield test_client
