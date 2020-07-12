from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wellread.app import app, get_db
from wellread.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()  # pylint: disable=no-member
        # Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_team():
    response = client.post(
        "/team/",
        json={
            "team_id": "T0140PRK962",
            "name": "WellRead",
            "domain": "www.domain.com",
            "email_domain": "",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    team_id = data["team_id"]
    assert team_id == "T0140PRK962"
    assert data["name"] == "WellRead"

    response = client.get(f"/team/{team_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "WellRead"
    assert data["team_id"] == team_id


# mock user id U014YSCLQ2X
