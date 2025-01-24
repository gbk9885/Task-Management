from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db  
from app.models.users_model import User 
from app.models.task_model import Task
from app.helpers.utility import get_current_user  

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"]
)

@router.get("")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Role-based dashboard.
    """
    # Fetch the user's role
    user_roles = [role.name.lower() for role in current_user.roles]

    # Admin Dashboard
    if "admin" in user_roles:
        return get_admin_dashboard(db)

    # Manager Dashboard
    if "manager" in user_roles:
        return get_manager_dashboard(db, current_user)

    # User Dashboard
    if "user" in user_roles:
        return get_user_dashboard(db, current_user)

    # If no valid role found
    raise HTTPException(status_code=403, detail="Access denied")

# Admin Dashboard
def get_admin_dashboard(db: Session):
    users = db.query(User).all()
    tasks = db.query(Task).all()  # Assuming Task is a model
    return {
        "dashboard": "Admin Dashboard",
        "users": [{"id": user.id, "username": user.username, "email": user.email} for user in users],
        "tasks": [{"id": task.id, "title": task.title, "status": task.status} for task in tasks],
    }

# Manager Dashboard
def get_manager_dashboard(db: Session, current_user: User):
    # Example: Managers see tasks assigned to their team
    tasks = db.query(Task).filter(Task.user_id.in_([user.id for user in current_user.team_members])).all()
    return {
        "dashboard": "Manager Dashboard",
        "tasks": [{"id": task.id, "title": task.title, "status": task.status} for task in tasks],
    }

# User Dashboard
def get_user_dashboard(db: Session, current_user: User):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return {
        "dashboard": "User Dashboard",
        "tasks": [{"id": task.id, "title": task.title, "status": task.status} for task in tasks],
    }
