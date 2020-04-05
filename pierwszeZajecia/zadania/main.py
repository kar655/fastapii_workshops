from fastapi import FastAPI
from pydantic import BaseModel
from responses import *

app = FastAPI()
app.patietn_id = 0;

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
	app.patietn_id += 1
	return PatientResp(id=app.patietn_id - 1, patient=new_patient)