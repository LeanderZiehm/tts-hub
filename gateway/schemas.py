from pydantic import BaseModel

class UserCreateResponse(BaseModel):
    api_key: str
    credits: int