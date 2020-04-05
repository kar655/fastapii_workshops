from fastapi.testclient import TestClient
import pytest

from main import app
from responses import RootResponse

client = TestClient(app)


def test_root():
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == RootResponse(message="Hello World during the coronavirus pandemic!")