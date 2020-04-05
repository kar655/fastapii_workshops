from fastapi.testclient import TestClient
import pytest

from main import app
from responses import *

client = TestClient(app)


def test_root():
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == RootResponse(message="Hello World during the coronavirus pandemic!")

def test_method_get():
	response = client.get("/method")
	assert response.status_code == 200
	assert response.json() == MethodResponse(method="GET")

def test_method_post():
	response = client.post("/method")
	assert response.status_code == 200
	assert response.json() == MethodResponse(method="POST")

def test_method_put():
	response = client.put("/method")
	assert response.status_code == 200
	assert response.json() == MethodResponse(method="PUT")

def test_method_delete():
	response = client.delete("/method")
	assert response.status_code == 200
	assert response.json() == MethodResponse(method="DELETE")


def test_add_patient_one():
	new_patient = PatientReq(name="Ola", surename="Kowalska")
	response = client.post("/patient", json=new_patient.dict())
	assert response.status_code == 200
	assert response.json() == PatientResp(id=0, patient=new_patient).dict()


def test_add_patient_two():
	new_patient = PatientReq(name="Ząb", surename="Żółty")
	response = client.post("/patient", json=new_patient.dict())
	assert response.status_code == 200
	assert response.json() == PatientResp(id=1, patient=new_patient).dict()