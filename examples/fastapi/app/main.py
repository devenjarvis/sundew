# FastAPI Example
# Source: https://fastapi.tiangolo.com/advanced/async-sql-databases/?h=sqlite

from typing import Any

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Setup db
DATABASE_URL = "sqlite:///./fastapi_example.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


# Models
class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int  # noqa: A003
    text: str
    completed: bool


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


@app.get("/notes/", response_model=list[Note])
async def read_notes() -> list[databases.interfaces.Record]:
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn) -> dict[str, Any]:
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}
