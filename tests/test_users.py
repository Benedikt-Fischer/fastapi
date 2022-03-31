from app import schemas
from jose import JWTError, jwt
#from tests.database import client, session
from app.config import settings
import pytest

def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json().get('message') == 'Hello Word!??!'

def test_create_user(client):
    res = client.post("/users/", json={'email': 'hello123@gmail.com', 'password': 'password123'})
    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == 'hello123@gmail.com'

def test_login_user(client, test_user):
    res = client.post("/login", data={'username': test_user['email'], 'password':  test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    user_id: str = payload.get("user_id")
    assert user_id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200