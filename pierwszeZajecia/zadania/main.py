from fastapi import FastAPI, HTTPException, Response, Cookie, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from responses import *
from hashlib import sha256
import secrets

app = FastAPI()
app.secret_key = "random text"
app.patient_id = 0
app.patients = []

security = HTTPBasic()



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

	if secrets.compare_digest(credentials.username, "trudnY") and \
		secrets.compare_digest(credentials.password, "PaC1Ent"):

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
def get_patient(id: int):
	if id < 0 or id >= app.patient_id:
		raise HTTPException(status_code=204, detail="No Content")
	return app.patients[id]