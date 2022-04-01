from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import models
from app.config import settings
from app.database import get_db
from app.oauth2 import create_access_token

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

@pytest.fixture
def test_user(client):
    user_data = {'email': 'hello123@gmail.com', 'password': 'password123'}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {'email': 'abc@gmail.com', 'password': 'abc'}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post_data):
        return models.Post(**post_data)

    posts_map = map(create_post_model, post_data)
    posts = list(posts_map)

    session.add_all(posts)

    session.commit()

    posts_response = session.query(models.Post).all()
    return posts_response
