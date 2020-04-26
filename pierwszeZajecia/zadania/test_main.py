from fastapi.testclient import TestClient
import pytest

from main import app
from responses import *

client = TestClient(app)


def test_root():
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == RootResponse(message="Hello World during the coronavirus pandemic!")

def test_welcome():
	response = client.get("/welcome")
	assert response.status_code == 200
	assert response.json() == WelcomeResponse(message="Welcome!")

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

def test_login_bad():
	response = client.post("/login", json={"login": "Ala", "password": "Kowalska"})
	assert response.status_code == 401
	assert response.json() == {"detail": "Not authenticated"}

def test_login_good():
	response = client.post("/login", json={"login": "trudnY", "password": "PaC13Nt"})
	assert response.status_code == 302

def test_add_patient_zero():
	new_patient = PatientReq(name="Ola", surename="Kowalska")
	response = client.post("/patient", json=new_patient.dict())
	assert response.status_code == 200
	assert response.json() == PatientResp(id=0, patient=new_patient).dict()


def test_add_patient_one():
	new_patient = PatientReq(name="Ząb", surename="Żółty")
	response = client.post("/patient", json=new_patient.dict())
	assert response.status_code == 200
	assert response.json() == PatientResp(id=1, patient=new_patient).dict()


def test_get_patient_one():
	new_patient = PatientReq(name="Ząb", surename="Żółty")
	response = client.get("/patient/1")
	assert response.status_code == 200
	assert response.json() == new_patient.dict()

def test_get_patient_negative():
	response = client.get("/patient/-3")
	assert response.status_code == 204
	assert response.json() == {"detail": "No Content"}


def test_get_patient_too_big():
	response = client.get("/patient/323")
	assert response.status_code == 204
	assert response.json() == {"detail": "No Content"}
