from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest


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





SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_ip_address}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingsessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


