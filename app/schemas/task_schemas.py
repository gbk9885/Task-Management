from pydantic import BaseModel

# Pydantic models for validation
class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUser(BaseModel):
    user_id: int

class TaskStatus(BaseModel):
    status: str

class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str
    username: str

    