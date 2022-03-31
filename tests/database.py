from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import models
from app.config import settings
from app.database import get_db

SQLALCHEMY_DATABASE_URL = (f"postgresql://{settings.database_username}:"
                           f"{settings.database_password}@{settings.database_hostname}:"
                           f"{settings.database_port}/{settings.database_name}_test")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()

def override_get_db():
    """Try to return session to database"""
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()

app.dependency_overrides[get_db] = override_get_db

#client = TestClient(app)

@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)