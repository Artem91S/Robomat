import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Config
from app.core.db_connection import Base, get_db
from app.main import app
import uuid
from datetime import datetime
from app.models.events import EventDB

engine = create_engine(Config.TEST_DB_URL)

TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture()
def test_client():

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSession()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def test_event_data():
    return {
        "event_id": str(uuid.uuid4()),
        "occurred_at": datetime.now().isoformat(),
        "user_id": 9999,
        "event_type": "test",
        "properties": {"item_id": "SKU2710", "length": 123},
    }
