from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

PRODUCTION_DB = getenv("PRODUCTION_DB")
USER = getenv("DB_USERNAME")
PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")

if PRODUCTION_DB == "postgres":
    SQLALCHEMY_DATABASE_URL = (
        f"postgres://{USER}:{PASSWORD}@{DB_HOST}:{DB_PORT}/wellread_db"
    )
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class WellReadBase(object):
    def update(self, non_null_updates: dict) -> None:
        """
        Custom DICT -> SQL update method
        Only safe for non-null setting. 
        More validation needed if nulling a column potentially
        """
        for key, value in non_null_updates.items():
            if hasattr(self, key):
                setattr(self, key, value)


Base = declarative_base()
