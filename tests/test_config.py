import os


def set_env():
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"


set_env()
