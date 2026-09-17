from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingsessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)





SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_ip_address}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingsessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)








def test_root(client, session):
    session.query()
    res = client.get("/")
    print(res.json())
    assert res.json().get("message") == "Hello World from Togliatti Rome!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users", json={"email" : "alamin@email.com", "password" : "password1234"})

    print(res.json())
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "alamin@email.com"
    assert res.status_code == 201