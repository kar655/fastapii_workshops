from fastapi import FastAPI, HTTPException, Response, Cookie, Depends, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List
from responses import *
from hashlib import sha256
import secrets
import sqlite3
import operator


app = FastAPI()
app.secret_key = "random text"
app.patient_id = 0
app.patients = []

app.key = sha256(bytes(f"trudnYPaC1Entrandom text",encoding="utf8")).hexdigest()

security = HTTPBasic()



@app.on_event("startup")
async def startup():
	app.db_connection = sqlite3.connect('chinook.db')


@app.on_event("shutdown")
async def shutdown():
	app.db_connection.close()


@app.get("/", response_model=RootResponse)
def root():
	return RootResponse(message="Hello World during the coronavirus pandemic!")

@app.get("/welcome", response_model=WelcomeResponse)
def welcome():
	return WelcomeResponse(message="Welcome!")

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



# def check_user(credentials: HTTPBasicCredentials = Depends(security)):

# 	correct_username = secrets.compare_digest(credentials.username, "trudnY")
# 	correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")

# 	if not (correct_username and correct_password):
# 		raise HTTPException(
# 			status_code=status.HTTP_401_UNAUTHORIZED
# 		)

# 	return credentials



# @app.post("/login")
# def login(response: Response, credentials = Depends(check_user)):

# 	session_token = sha256(bytes(f"{credentials.username}{credentials.password}",
# 		encoding="utf8")).hexdigest()

# 	# response = RedirectResponse(url="/welcome")

# 	response.set_cookie(key="session_token", value=session_token)
# 	response.status_code = status.HTTP_302_FOUND

# 	# return response
# 	return RedirectResponse(url="/welcome")


@app.post("/login", status_code=status.HTTP_302_FOUND)
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):

	if secrets.compare_digest(credentials.username, "trudnY") and secrets.compare_digest(credentials.password, "PaC1Ent"):

		session_token = sha256(bytes(
			f"{credentials.username}{credentials.password}{app.secret_key}",
			encoding="utf8")).hexdigest()

		response = RedirectResponse(url='/welcome')
		response.set_cookie(key="session_token", value=session_token)
		response.status_code = status.HTTP_302_FOUND
		return response

	else:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)



@app.get("/patient/{id}", response_model=PatientReq)
def get_patient(id: int, session_token: str = Cookie(None)):
	# if session_token != app.key:
	# 	raise HTTPException(status_code=403, detail="Unathorised")
	if id < 0 or id >= app.patient_id:
		raise HTTPException(status_code=204, detail="No Content")
	return app.patients[id]




@app.post("/logout")
def create_cookie(*, response: Response, session_token: str = Cookie(None)):
	# print(response)
	# print(session_token)
	if session_token != app.key :
		raise HTTPException(status_code=403, detail="Unathorised")
	response.set_cookie(key="session_token", value="0")


@app.get("/tracks")#/{page}/{per_page}") #response_model=List[Track])
async def get_tracks(page: int = 0, per_page: int = 10):
	app.db_connection.row_factory = sqlite3.Row
	# data = app.db_connection.execute("SELECT * FROM tracks LIMIT 10").fetchall()
	data = app.db_connection.execute(
		"SELECT * FROM tracks LIMIT ? OFFSET ?", (per_page, page, )).fetchall()

	# data = app.db_connection.execute(
	# 	f"SELECT * FROM tracks LIMIT {per_page}").fetchall()

	# print(data)
	return data;


@app.get("/tracks/composers")
async def get_composers(composer_name: str):
	# app.db_connection.row_factory = sqlite3.Row
	app.db_connection.row_factory = lambda cursor, x: x[0]

	data = app.db_connection.execute(
		"SELECT tracks.Name FROM tracks WHERE tracks.Composer = ? ORDER BY tracks.Name", (composer_name,)).fetchall()

	if len(data) == 0:
		raise HTTPException(status_code=404, detail="error")
	else:
		return data


@app.post("/albums", response_model=AlbumResponse, status_code=201)
async def post_album(new_album: NewAlbum):
	app.db_connection.row_factory = sqlite3.Row
	artist = app.db_connection.execute(
		"SELECT artists.ArtistId FROM artists WHERE artists.ArtistId = ?", (new_album.artist_id, )).fetchone()

	if artist == None:
		raise HTTPException(status_code=404, detail="error")

	cursor = app.db_connection.execute(
		"INSERT INTO albums (Title, ArtistId) VALUES (?, ?)", (new_album.title, new_album.artist_id,))
	app.db_connection.commit()
	new_album_id = cursor.lastrowid

	return AlbumResponse(AlbumId=new_album_id, Title=new_album.title, ArtistId=new_album.artist_id)


@app.get("/albums/{album_id}", response_model=AlbumResponse)
async def get_album(album_id: int):
	app.db_connection.row_factory = sqlite3.Row
	album = app.db_connection.execute(
		"SELECT * FROM albums WHERE albums.AlbumId = :AlbumId", {"AlbumId": album_id}).fetchone() #(album_id,)).fetchone()

	if album == None:
		raise HTTPException(status_code=404, detail="error")

	return album


# @app.patch("/items/{item_id}", response_model=Item)
# async def update_item(item_id: str, item: Item):
#     stored_item_data = items[item_id]
#     stored_item_model = Item(**stored_item_data)
#     update_data = item.dict(exclude_unset=True)
#     updated_item = stored_item_model.copy(update=update_data)
#     items[item_id] = jsonable_encoder(updated_item)
#     return updated_item

@app.put("/customers/{customer_id}", response_model=CustomerResponse)
async def update_customer(customer_id: int, new_customer: CustomerUpdate):

	new_customer = CustomerUpdateUpper(
		Company=new_customer.company, 
		Address=new_customer.address, 
		City=new_customer.city, 
		State=new_customer.state, 
		Country=new_customer.country, 
		PostalCode=new_customer.postalcode, 
		Fax=new_customer.fax)

	# print("PROCESSING")
	app.db_connection.row_factory = sqlite3.Row
	old_customer = app.db_connection.execute(
		"SELECT * FROM customers WHERE customers.CustomerId = ?", (customer_id,)).fetchone()

	if old_customer == None:
		raise HTTPException(status_code=404, detail="error")

	# print(f"\n{dict(old_customer)=}")

	old_customer_data = dict(old_customer)
	old_customer_model = CustomerResponse(**old_customer_data)
	# print(f"\n{old_customer_model=}")

	update_data = new_customer.dict(exclude_unset=True)
	# print(f"\n{update_data=}")

	update_item = old_customer_model.copy(update=update_data)
	# print(f"\n{old_customer_model=}")
	# print(f"\n{old_customer_model.copy(update=update_data)=}")

	# print("\n\n\n")
	# print(f"\n{update_item=}")
	# print("\n\n\n")
	# print(f"{jsonable_encoder(update_item)=}")

	# print(f"\n{update_item.dict()=}")
	nowe = CustomerUpdateUpper(**update_item.dict()).dict()
	nowe.update({"CustomerId": old_customer_model.CustomerId})

	# print(f"\n{nowe=}")

	cursor = app.db_connection.execute(
		"UPDATE customers SET Company = :Company, Address = :Address,\
		City = :City, State = :State, Country = :Country,\
		PostalCode = :PostalCode, Fax = :Fax \
		WHERE customers.CustomerId = :CustomerId", nowe)

	app.db_connection.commit()


	# old_customer21 = app.db_connection.execute(
	# 	"SELECT * FROM customers WHERE customers.CustomerId = ?", (customer_id,)).fetchone()

	# print(f"\n{tuple(old_customer21)=}")

	# return update_item
	# return old_customer_model

	result = app.db_connection.execute(
		"SELECT * FROM customers WHERE customers.CustomerId = ?", (customer_id,)).fetchone()
	return result


@app.get("/sales", response_model=List[SalesResponse])
async def get_sales(request: Request):
	# print(f"{request.query_params=}")

	if "category" not in request.query_params.keys() or request.query_params['category'] != 'customers':
		raise HTTPException(status_code=404, detail="error")

	# print(f"{request.query_params['category']=}")

	#ids = [int(x) for x in request.query_params['category']]
	# print(f"{ids=}")

	# Parametr ?category=customers zwróci statystykę wydatków poszczególnych klientów sklepu,
	 # wraz z ich numerem id, adresem email i numerem telefonu, RODO rules ;) .


 #    Wyniki mają być filtrowane po sumie wydatków od największych oraz po numerze id klienta.

 #    Suma powinna być zaokrąglona do 2-ch miejsc po przecinku.


# SELECT tracks.name, artists.name FROM tracks
# JOIN albums ON tracks.albumid = albums.albumid
# JOIN artists ON albums.artistid = artists.artistid;

	app.db_connection.row_factory = sqlite3.Row
	# data = app.db_connection.execute(
	# 	"SELECT customers.CustomerId, customers.Email, customers.Phone, invoices.Total AS Sum FROM customers \
	# 	JOIN invoices ON customers.CustomerId = invoices.CustomerId \
	# 	ORDER BY invoices.Total DESC, customers.CustomerId ASC").fetchall()# \
	data = app.db_connection.execute(
	"SELECT customers.CustomerId, customers.Email, customers.Phone, invoices.Total AS Sum FROM customers \
	JOIN invoices ON customers.CustomerId = invoices.CustomerId \
	ORDER BY customers.CustomerId ASC").fetchall()# \


	# print(f"{data=}")

	first = True
	result = []
	lastSum = 0
	lastCustomer = None

	for x in data:
		if first:
			lastCustomer = x
			lastSum = x[3]
			first = False
			continue

		if x[0] == lastCustomer[0]:
			lastSum += x[3]
		else:
			result.append(
			SalesResponse(CustomerId=lastCustomer[0], Email=lastCustomer[1], Phone=lastCustomer[2], Sum=round(lastSum, 2))
			)
			lastSum = 0
			lastCustomer = x


		# result.append(
		# 	SalesResponse(CustomerId=x[0], Email=x[1], Phone=x[2], Sum=x[3])
		# 	)

	# add last guy
	result.append(
	SalesResponse(CustomerId=lastCustomer[0], Email=lastCustomer[1], Phone=lastCustomer[2], Sum=round(lastSum + lastCustomer[3], 2))
	)

	result_sorted = sorted(result, key=operator.attrgetter("CustomerId"), reverse=True)
	result_sorted = sorted(result_sorted, key=operator.attrgetter("Sum"), reverse=True)

	return result_sorted

	# return data