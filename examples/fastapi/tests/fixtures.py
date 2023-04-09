from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path

import databases
from app import main
from httpx import AsyncClient


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
async def test_client() -> AsyncIterator:
    async with AsyncClient(app=main.app, base_url="http://test") as test_client:
        yield test_client
