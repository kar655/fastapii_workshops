from fastapi import FastAPI, HTTPException, Response, Cookie, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List
from responses import *
from hashlib import sha256
import secrets
import sqlite3

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