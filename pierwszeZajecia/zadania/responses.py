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

class LoginReq(BaseModel):
	login: str
	password: str

class PatientResp(BaseModel):
	id: int
	patient: PatientReq


class Track(BaseModel):
	TrackId: int
	Name: str
	AlbumId: int
	MediaTypeId: int
	GenreId: int
	Composer: str
	Milliseconds: int
	Bytes: int
	UnitPrice: float