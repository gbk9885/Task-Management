from pydantic import BaseModel
# Pydantic model to define registration data

class UserLogin(BaseModel):
    username: str
    password: str
class UserCreate(UserLogin):
    email: str
    role_name: str
    name:str