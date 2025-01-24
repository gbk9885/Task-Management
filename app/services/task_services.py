from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.task_model import Task
from app.models.users_model import User
from app.db import get_db
from app.schemas.task_schemas import TaskCreate,TaskUser,TaskStatus,TaskUpdate
from app.helpers.utility import get_current_user,get_user_role_name



router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Get the logged-in user
):
    # Check if the user has 'manager' or 'admin' role
    if not any(role.name in ['Manager', 'Admin'] for role in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create tasks"
        )

    # Ensure the user exists
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the task
    new_task = Task(
        title=task.title,
        description=task.description,
        user_id=current_user.id
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created successfully", "task": new_task}


@router.put("/{task_id}/assign")
def assign_task(task_user : TaskUser,task_id: int, 
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
     # Check if the user has 'manager' or 'admin' role
    if not any(role.name in ['Manager', 'Admin'] for role in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create tasks"
        )
    # Check if task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if the new user exists
    user = db.query(User).filter(User.id == task_user.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Assign the task to the new user
    task.user_id = task_user.user_id
    db.commit()
    db.refresh(task)

    return {"message": "Task assigned successfully", "task": task}

@router.put("/{task_id}/status")
def update_task_status(task_id: int, taskstatus:TaskStatus, db: Session = Depends(get_db)):
    # Validate status
    if taskstatus.status not in ['New','Pending', 'Inprogress', 'Completed']:
        raise HTTPException(status_code=400, detail="Invalid status")

    # Check if task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task status
    task.status = taskstatus.status
    db.commit()
    db.refresh(task)

    return {"message": "Task status updated", "task": task}

@router.put("/{task_id}")
def update_task(
    task_id: int, 
    task_update: TaskUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Update task with title, status, description, and assignee.
    """
    # Check if the user has 'manager' or 'admin' role
    if not any(role.name in ['Manager', 'Admin'] for role in current_user.roles) and current_user.username != task_update.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update tasks"
        )

    # Check if task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task details
    task.title = task_update.title
    task.description = task_update.description
    task.status = task_update.status
    user_id = db.query(User.id).filter(User.username == task_update.username).first()
    task.user_id = user_id[0]

    db.commit()
    db.refresh(task)

    return {"message": "Task updated successfully", "task": task}

@router.get("/stats")
def get_task_statistics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get statistics about tasks for the logged-in user.
    If the user is an Admin or Manager, return all tasks. 
    If the user is a User, return only their assigned tasks.
    """
    
    # Check the role of the logged-in user
    current_user_role = get_user_role_name(db, current_user.id)
    if current_user_role == "Admin" or current_user_role == "Manager":
        tasks = db.query(Task).all()  # Get all tasks if the user is Admin or Manager
    elif current_user_role == "User":
        tasks = db.query(Task).filter(Task.user_id == current_user.id).all()  # Get only tasks assigned to the user
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Extract task statistics
    tasks_dict = [task.__dict__ for task in tasks]
    new_count = sum(1 for task in tasks_dict if task["status"] == "New")
    pending_count = sum(1 for task in tasks_dict if task["status"] == "Pending")
    completed_count = sum(1 for task in tasks_dict if task["status"] == "Completed")
    in_progress_count = sum(1 for task in tasks_dict if task["status"] == "In Progress")

    return {
        "new": new_count,
        "pending": pending_count,
        "completed": completed_count,
        "in_progress": in_progress_count,
    }

@router.get("")
def get_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all tasks based on the user's role.
    If the user is an Admin or Manager, return all tasks.
    If the user is a User, return only their assigned tasks.
    """
    current_user_role = get_user_role_name(db, current_user.id)
    if current_user_role in ["Admin", "Manager"]:
        tasks = db.query(Task).all()
        # Add username to each task
        for task in tasks:
            user = db.query(User).filter(User.id == task.user_id).first()
            task.username = user.username if user else None
    elif current_user_role == "User":
        tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    return tasks

@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Get the user associated with the task
    user = db.query(User).filter(User.id == task.user_id).first()
    if user:
        task_details = task.__dict__
        task_details["username"] = user.username
    else:
        task_details = task.__dict__
        task_details["username"] = None

    return task_details

