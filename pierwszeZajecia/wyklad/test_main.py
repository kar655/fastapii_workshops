
from fastapi.testclient import TestClient

import pytest

from main import app, HelloResp




client = TestClient(app)


def test_read_main():
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == {"message": "Hello World"}


@pytest.mark.parametrize("name", ["Zenek", "Ola", "Jan Kowalski", "Żółty"])
def test_hello_name(name):
	response = client.get(f"/hello/{name}")
	assert response.status_code == 200
	# print(response.text)
	assert response.json() == {"msg":f"Hello {name}"}

def test_receive_something():
	response = client.post("/dej/mi/coś", json={'first_key': 'some_value'})
	assert response.json() == {"received": {'first_key': 'some_value'},
								"constant_data": "python jest super"}