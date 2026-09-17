from app import schemas
from database import client,session



def test_root(client, session):
    session.query()
    res = client.get("/")
    print(res.json())
    assert res.json().get("message") == "Hello World from Togliatti Rome!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users", json={"email": "hello123@gmail.com", "password": "password123"})

    new_user = schemas.UserResponse(**res.json())
    print(new_user)
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_user_login(client):
    res = client.post("/login", data={"username": "hello123@gmail.com", "password": "password123"})

    print(res.json())
    assert res.status_code == 200


