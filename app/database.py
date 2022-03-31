"""
Define, create and return session to database
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = (f"postgresql://{settings.database_username}:"
                           f"{settings.database_password}@{settings.database_hostname}:"
                           f"{settings.database_port}/{settings.database_name}")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Try to return session to database"""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
        