import os
import json
from typing import Generator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL
import boto3
from dotenv import load_dotenv
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Load environment variables from .env file
load_dotenv()


def init_secrets_manager_client() -> boto3.client:
    """
    Initialize and return the AWS Secrets Manager client.

    :return: AWS Secrets Manager client.
    :rtype: boto3.client
    """
    return boto3.client('secretsmanager', region_name=os.getenv('AWS_DEFAULT_REGION'))


def get_secret(secret_name: str) -> dict:
    """
    Retrieve a secret from AWS Secrets Manager.

    :param secret_name: The name of the secret to retrieve.
    :type secret_name: str
    :return: The secret value as a dictionary.
    :rtype: dict
    """
    client = init_secrets_manager_client()
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])

    # Log the keys of the secret (avoid logging sensitive values)
    logger.debug(f"Retrieved secret keys: {list(secret.keys())}")

    return secret


# Retrieve database credentials from secrets
secret_name = 'insurance-policy-db-credentials'
db_credentials = get_secret(secret_name)

DB_USER = db_credentials.get("username")
DB_PASSWORD = db_credentials.get("password")
DB_HOST = db_credentials.get("host")
DB_PORT = db_credentials.get("port")
DB_NAME = db_credentials.get("dbname")
DB_SCHEMA = db_credentials.get("schema", "public")

# Construct the database URL
DATABASE_URL = os.getenv("DATABASE_URL") or f"postgresql+pg8000://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Log the constructed URL without credentials
logger.debug(f"DATABASE_URL (without credentials): postgresql+pg8000://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


def create_engine_and_metadata(url: str) -> tuple:
    """
    Create and return SQLAlchemy engine and metadata based on the URL.

    :param url: Database URL to configure the engine.
    :type url: str
    :return: A tuple containing the SQLAlchemy engine and metadata.
    :rtype: tuple
    """
    if url.startswith("sqlite"):
        return create_engine(url, echo=True), MetaData()

    return create_engine(URL.create(
        drivername="postgresql+pg8000",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )), MetaData(schema=DB_SCHEMA)


engine, metadata = create_engine_and_metadata(DATABASE_URL)

# Create a session maker and a base class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=metadata)


def get_db() -> Generator[SessionLocal, None, None]:
    """
    Provide a database session.

    :return: A generator yielding a database session.
    :rtype: Generator[SessionLocal, None, None]
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
