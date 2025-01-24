from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.task_model import Task
from app.db import get_db
from app.models.users_model import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}/tasks")
def get_user_tasks(user_id: int, db: Session = Depends(get_db)):
    # Fetch tasks assigned to the user
    tasks = db.query(Task).filter(Task.user_id == user_id).all()

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this user")

    return {"tasks": tasks}

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    # Fetch all users
    users = db.query(User).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return {"users": users}

