from pydantic import BaseModel
from typing import Optional

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

class NewAlbum(BaseModel):
	title: str
	artist_id: int

class AlbumResponse(BaseModel):
	AlbumId: int
	Title: str
	ArtistId: int

class CustomerUpdate(BaseModel):
	company: str = None
	address: str = None
	city: str = None
	state: str = None
	country: str = None
	postalcode: str = None
	fax: str = None

class CustomerUpdateUpper(BaseModel):
	Company: str = None
	Address: str = None
	City: str = None
	State: str = None
	Country: str = None
	PostalCode: str = None
	Fax: str = None

class CustomerResponse(BaseModel):
	CustomerId: int = 0
	FirstName: str = None
	LastName: str = None
	Company: str = None
	Address: str = None
	City: str = None
	State: str = None
	Country: str = None
	PostalCode: str = None
	Phone: str = None
	Fax: str = None
	Email: str = None
	SupportRepId: int = 0


class CustomerResponseLower(BaseModel):
	customerid: int = 0
	firstname: str = None
	lastname: str = None
	company: str = None
	address: str = None
	city: str = None
	state: str = None
	country: str = None
	postalcode: str = None
	phone: str = None
	fax: str = None
	email: str = None
	supportrepid: int = 0


class SalesResponse(BaseModel):
	CustomerId: int
	Email: str
	Phone: Optional[str]
	Sum: float