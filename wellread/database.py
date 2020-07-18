from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class WellReadBase(object):
    def update(self, non_null_updates: dict):
        """
        Custom DICT -> SQL update method
        Only safe for non-null setting. 
        More validation needed if nulling a column potentially
        """
        for key, value in non_null_updates.items():
            if hasattr(self, key):
                setattr(self, key, value)


Base = declarative_base()
