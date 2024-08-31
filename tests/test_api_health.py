from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.health.routes import router

api = FastAPI()
api.include_router(router)

client = TestClient(api)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
