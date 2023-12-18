import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(dotenv_path=".env.dev")

DATABASE_URL = os.getenv("DEV_DATABASE_URI")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create the SQLAlchemy Base object
Base = declarative_base()

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
