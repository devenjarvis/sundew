import databases
import ormar
import sqlalchemy

database = databases.Database("sqlite:///db.sqlite")
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class Notes(ormar.Model):
    class Meta(BaseMeta):
        tablename = "notes"

    id: int = ormar.Integer(primary_key=True, autoincrement=True)  # noqa: A003
    text: str = ormar.String(max_length=1024)
    completed: bool = ormar.Boolean()
