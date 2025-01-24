from fastapi import APIRouter,Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.db import get_db
from app.helpers.utility import get_user_by_username,verify_password,create_access_token,get_user_role_name
from app.schemas.user_schema import UserLogin

router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not found"}},
)

@router.post("")
def login_user(user:UserLogin, db: Session = Depends(get_db)):
    user_db = get_user_by_username(db, user.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist."
        )

    if not verify_password(user.password, user_db.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )
    access_token = create_access_token(data={"sub": user.username})
    user_role_name = get_user_role_name(db, user_db.id)

    # Add a dynamic property to the user_db object
    user_db.role = user_role_name  # Dynamically attach the role name

    return {"access_token": access_token, "token_type": "bearer","user":user_db}