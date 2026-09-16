from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json())
    assert res.json().get("message") == "Hello World from Togliatti Rome!"
    assert res.status_code == 200

def test_create_user():
    res = client.post("/users", json={"email" : "alamin@email.com", "password" : "password1234"})

    print(res.json())
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "alamin@email.com"
    assert res.status_code == 201