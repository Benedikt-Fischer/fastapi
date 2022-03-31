import pytest
from app import schemas
from jose import jwt
#from tests.database import client, session
from app.config import settings

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

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongmail@gmail.com', 'password123', 403),
    ('hello123@gmail.com', 'wrongpassword', 403),
    ('wrongmail@kek.c', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('hello123@gmail.com', None, 422),
    (None, None, 422),
    ('', 'password123', 422),
    ('s', 'password123', 403)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={'username': email, 'password':  password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'