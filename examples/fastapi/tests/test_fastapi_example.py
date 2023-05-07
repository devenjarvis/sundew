from app import db, main
from fixtures import add_sample_notes, test_sqlite_db

from sundew import test

test(main.read_notes)(
    patches={"app.db.BaseMeta.database": test_sqlite_db},
    returns=[],
)

test(main.create_note)(
    patches={"app.db.BaseMeta.database": test_sqlite_db},
    kwargs={"note": main.NoteIn(text="test", completed=False)},
    returns=db.Notes(id=1, text="test", completed=False),
)

test(main.read_notes)(
    patches={"app.db.BaseMeta.database": test_sqlite_db},
    setup=[add_sample_notes],
    returns=[
        db.Notes(id=1, text="test", completed=False),
        db.Notes(id=2, text="test2", completed=True),
        db.Notes(id=3, text="test3", completed=False),
    ],
)
