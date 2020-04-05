from fastapi import FastAPI
from pydantic import BaseModel
from responses import RootResponse

app = FastAPI()

@app.get("/", response_model=RootResponse)
def root():
	return RootResponse(message="Hello World during the coronavirus pandemic!")

