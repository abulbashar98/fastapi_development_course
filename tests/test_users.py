from app import schemas
import pytest
from jose import jwt
from app.config import settings




def test_root(client, session):
    session.query()
    res = client.get("/")
    print(res.json())
    assert res.json().get("message") == "Hello World from Togliatti Rome!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users", json={"email": "hello123@gmail.com", "password": "password123"})

    new_user = schemas.UserResponse(**res.json())
    # print(new_user)
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_user_login(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    # print(login_res)
    payload = jwt.decode(login_res.access_token,settings.secret_access_key,algorithms=[settings.algorithm])

    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code",[
    ("signi@gmail.com", "wrongPassword", 403),
    ("wrongEmail@gmail.com", "password123", 403),
    ("wrongEmail@gmail.com", "wrongPassword@gmail.com", 403),
    (None, "password123", 422),
    ("signi@gmail.com", None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    # assert res.json().get('detail') == "Invalid Credentials"
    assert res.status_code == status_code
    


