from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert  res.status_code == 200
    assert res.json().get('message') == 'Hello Word!??!'

def test_create_user():
    res = client.post("/users/", json={'email': 'hello123@gmail.com', 'password': 'password123'})
    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == 'hello123@gmail.com'
