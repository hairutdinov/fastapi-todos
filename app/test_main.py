from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_create_item():
    data = {"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"}
    response = client.post("/items", json=data, headers={"X-Token": "coneofsilence"})
    assert response.status_code == 201
    assert response.json() == data
