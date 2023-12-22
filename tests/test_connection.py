from app.db.db_setup import engine


def test_connection():
    with engine.connect() as conn:
        pass
