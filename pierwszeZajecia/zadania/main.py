from fastapi import FastAPI
from pydantic import BaseModel
from responses import *

app = FastAPI()

@app.get("/", response_model=RootResponse)
def root():
	return RootResponse(message="Hello World during the coronavirus pandemic!")



@app.get("/method",response_model=MethodResponse)
def method():
	return MethodResponse(method="GET")

@app.post("/method",response_model=MethodResponse)
def method():
	return MethodResponse(method="POST")

@app.put("/method",response_model=MethodResponse)
def method():
	return MethodResponse(method="PUT")

@app.delete("/method",response_model=MethodResponse)
def method():
	return MethodResponse(method="DELETE")