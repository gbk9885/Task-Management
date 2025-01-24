from fastapi import APIRouter,Depends, HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db import get_db
from app.helpers.utility import hash_password
from app.models.users_model import User
from app.models.user_role_model import user_roles
from app.models.role_model import Role
from app.schemas.user_schema import UserCreate
from sqlalchemy import func


router = APIRouter(
    prefix="/register",
    tags=["register"],
    responses={404: {"description": "Not found"}},
)


@router.post("", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(or_(User.username == user.username,User.email == user.email)).first()
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use"
        )

    # You can add password hashing here
    hashed_password = hash_password(user.password)
    user_db = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    # Retrieve the role (e.g., 'user' role, could be dynamic)
    role = db.query(Role).filter(func.lower(Role.name) == func.lower(user.role_name)).first() # Or assign a specific role dynamically

    if not role:
        raise Exception("Role not found")
    user_role = {
        "user_id": user_db.id,
        "role_id": role.id
    }
    db.execute(user_roles.insert().values(user_role))  # This will insert into user_roles
    db.commit()

    return {"message": "User registered successfully."}