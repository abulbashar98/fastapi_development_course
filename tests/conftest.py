from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest
from app.oAuth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_ip_address}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingsessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingsessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
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
    user_data = {"email": "signi@gmail.com", "password": "password123"}
    res = client.post("/users", json=user_data)
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    # print(new_user)
    assert res.status_code == 201
    return new_user

@pytest.fixture
def create_token(test_user):
    token = create_access_token({"user_id": test_user['id']})
    return token

@pytest.fixture
def authorized_client(create_token, client):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {create_token}"
    }

    return client

@pytest.fixture
def test_posts(session, test_user):
    post_data = [
        {"title": "1st post title", "content": "1st post content", "owner_id": test_user['id'], "phone_number": "0123541515", "address": "Rome Termini"},
        {"title": "2nd post title", "content": "2nd post content", "owner_id": test_user['id'], "phone_number": "0123541515", "address": "Rome Termini"},
        {"title": "3rd post title", "content": "3rd post content", "owner_id": test_user['id'], "phone_number": "0123541515", "address": "Rome Termini"}
    ]

    def create_post_model(post):
        return models.Post(**post)

    # map(func, Iterable)s
    post_map = map(create_post_model, post_data)
    posts = list(post_map)



    session.add_all(posts)
    # session.add_all([
    #     models.Post(title = "1st post title", content = "1st post content", owner_id = test_user['id']),
    #     models.Post(title = "2nd post title", content = "2nd post title", owner_id = test_user['id']),
    #     models.Post(title = "3rd post title", content = "3rd post content", owner_id = test_user['id'])
    # ])

    session.commit()

    posts = session.query(models.Post).all()
    return posts





