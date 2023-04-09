from app import main
from fixtures import test_sqlite_db

from sundew import AsyncTestClient, test

client = AsyncTestClient(app=main.app, base_url="http://testserver")


test(main.read_notes)(
    patches={"app.main.database": test_sqlite_db},
    returns=[(1, 2, 3)],
)
