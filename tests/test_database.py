import pytest
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from app.database import get_secret, get_db, engine

# Define the name of the secret you are fetching from AWS Secrets Manager
SECRET_NAME = 'insurance-policy-db-credentials'


@pytest.mark.integration
def test_get_secret():
    """Test fetching the secret directly from AWS Secrets Manager."""
    secret = get_secret(SECRET_NAME)

    assert 'username' in secret, "Missing 'username' in secret"
    assert 'password' in secret, "Missing 'password' in secret"
    assert 'host' in secret, "Missing 'host' in secret"
    assert 'port' in secret, "Missing 'port' in secret"
    assert 'dbname' in secret, "Missing 'dbname' in secret"


@pytest.mark.integration
def test_database_connection():
    """Test if the database connection can be established."""
    try:
        connection = engine.connect()
        connection.close()
        connection_success = True
    except OperationalError:
        connection_success = False

    assert connection_success, "Failed to connect to the database."


@pytest.mark.integration
def test_get_db():
    """Test the get_db generator to ensure it yields a session and closes it properly."""
    db_generator = get_db()
    session = next(db_generator)

    assert isinstance(session, Session)

    try:
        next(db_generator)
    except StopIteration:
        pass
