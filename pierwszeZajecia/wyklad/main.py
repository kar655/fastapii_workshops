
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()
app.counter = 0


class HelloResp(BaseModel):
	msg: str



@app.get("/")
def root():
	return {"message": "Hello World"}

@app.get("/counter")
def counter():
	app.counter += 1
	return str(app.counter)

@app.get("/hello/{name}", response_model=HelloResp)
async def read_item(name: str):
	return HelloResp(msg=f"Hello {name}")


class GiveMeSomethingRq(BaseModel):
	first_key: str

class GiveMeSomethingResp(BaseModel):
	received: Dict
	constant_data: str = "python jest super"

@app.post("/dej/mi/coś", response_model=GiveMeSomethingResp)
def receive_something(rq: GiveMeSomethingRq):
	return GiveMeSomethingResp(received=rq.dict())