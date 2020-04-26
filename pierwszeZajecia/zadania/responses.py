from pydantic import BaseModel

class RootResponse(BaseModel):
	message: str

class WelcomeResponse(BaseModel):
	message: str

class MethodResponse(BaseModel):
	method: str


class PatientReq(BaseModel):
	name: str
	surename: str


class PatientResp(BaseModel):
	id: int
	patient: PatientReq