# FastAPI Example
# Source: https://fastapi.tiangolo.com/advanced/async-sql-databases/?h=sqlite


from app.db import Notes, database
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()


# Models
class NoteIn(BaseModel):
    text: str
    completed: bool


@app.on_event("startup")
async def startup() -> None:
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    if database.is_connected:
        await database.disconnect()


@app.get("/notes/", response_model=list[Notes])
async def read_notes() -> list[Notes]:
    return await Notes.objects.select_all().all()


@app.post("/notes/", response_model=Notes)
async def create_note(note: NoteIn) -> Notes:
    return await Notes.objects.create(text=note.text, completed=note.completed)
