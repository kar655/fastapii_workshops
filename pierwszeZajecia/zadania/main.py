from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from responses import *

app = FastAPI()
app.patient_id = 0
app.patients = []

@app.get("/", response_model=RootResponse)
def root():
	return RootResponse(message="Hello World during the coronavirus pandemic!")



@app.get("/method", response_model=MethodResponse)
def method():
	return MethodResponse(method="GET")

@app.post("/method", response_model=MethodResponse)
def method():
	return MethodResponse(method="POST")

@app.put("/method", response_model=MethodResponse)
def method():
	return MethodResponse(method="PUT")

@app.delete("/method", response_model=MethodResponse)
def method():
	return MethodResponse(method="DELETE")


@app.post("/patient", response_model=PatientResp)
def add_patient(new_patient: PatientReq):
	app.patient_id += 1
	app.patients.append(new_patient)
	return PatientResp(id=app.patient_id - 1, patient=new_patient)

@app.get("/patient/{id}", response_model=PatientReq)
def get_patient(id: int):
	if id < 0 or id >= app.patient_id:
		raise HTTPException(status_code=404, detail="Item not found")
	return app.patients[id]