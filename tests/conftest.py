import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.dependencies import get_db, get_current_user
from app.db.base_class import Base
from app import models
from app.models.user import User

@pytest.fixture
def temp_session(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture
def client(temp_session):
    # create a user
    db = temp_session()
    user = User(username="tester", email="tester@example.com", hashed_password="fake")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.expunge(user)
    db.close()

    def override_get_db():
        db = temp_session()
        try:
            yield db
        finally:
            db.close()

    def override_get_current_user():
        return user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    client = TestClient(app)
    yield client, temp_session
    app.dependency_overrides = {}

