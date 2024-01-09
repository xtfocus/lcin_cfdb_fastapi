import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv(dotenv_path=".env.dev")

LOGIN_DB_URL = os.getenv("LOGIN_DATABASE_URI")

# Create the SQLAlchemy engine
engine = create_engine(LOGIN_DB_URL)

# create the SessionLocal class. This is not yet a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is a class. Later we can inherit from this class to
# create each of the database models or classes (the ORM models):
Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
