import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.policy.models import Policy
from app.api.policy.routes import router
from app.database import engine, Base, get_db

api = FastAPI()
api.include_router(router)

# Create a TestClient instance
client = TestClient(api)


@pytest.fixture(scope='session', autouse=True)
def setup_database():
    """Setup and teardown the database for tests."""
    print("Setting up the database...")
    Base.metadata.create_all(bind=engine)  # Create tables
    print("Tables created:", Base.metadata.tables.keys())

    # Add initial data
    db = next(get_db())
    try:
        # Adding a few policies
        policies = [
            Policy(name="Test Policy 1", coverage_amount=1000.0, premium=50.0),
            Policy(name="Test Policy 2", coverage_amount=2000.0, premium=75.0),
            Policy(name="Test Policy 3", coverage_amount=3000.0, premium=100.0)
        ]
        db.add_all(policies)
        db.commit()
    finally:
        db.close()

    yield

    print("Tearing down the database...")
    Base.metadata.drop_all(bind=engine)  # Drop tables after tests


@pytest.fixture
def create_test_policy():
    """Helper function to create a test policy."""
    db = next(get_db())
    try:
        policy = Policy(name="Test Policy", coverage_amount=1000.0, premium=50.0)
        db.add(policy)
        db.commit()
        db.refresh(policy)
        return policy
    finally:
        db.close()


def test_read_policies():
    """Test getting all policies."""
    response = client.get("/api/policies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_policy(create_test_policy):
    """Test getting a specific policy."""
    policy = create_test_policy
    response = client.get(f"/api/policies/{policy.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": policy.id,
        "name": policy.name,
        "coverage_amount": policy.coverage_amount,
        "premium": policy.premium
    }
