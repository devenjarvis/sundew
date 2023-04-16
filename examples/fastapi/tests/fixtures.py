from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path

import databases
from alembic import command
from alembic.config import Config
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

        alembic_cfg = Config()
        alembic_cfg.set_main_option(
            "script_location", str(Path(__file__).parents[1] / "app" / "migrations")
        )
        alembic_cfg.set_main_option("sqlalchemy.url", test_database_url)
        command.upgrade(alembic_cfg, "head")

        yield database

    finally:
        # delete temporary db
        new_db_file.unlink()


@asynccontextmanager
async def add_sample_notes() -> Iterator:
    try:
        # Add 3 rows
        await main.create_note(note=main.NoteIn(text="test", completed=False))
        await main.create_note(note=main.NoteIn(text="test2", completed=True))
        await main.create_note(note=main.NoteIn(text="test3", completed=False))
        yield
    finally:
        ...


@asynccontextmanager
async def test_client() -> AsyncIterator:
    async with AsyncClient(app=main.app, base_url="http://test") as test_client:
        yield test_client
