from pydantic import BaseModel

class RootResponse(BaseModel):
	message: str


class MethodResponse(BaseModel):
	method: str