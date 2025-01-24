from sqlalchemy.orm import  Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.models.users_model import User
from app.models.role_model import Role
from app.models.user_role_model import user_roles
from app.db import get_db
from fastapi import Depends, HTTPException, status
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

# This will be used to fetch the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Dependency to get the current user from JWT
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        # Fetch user from the database
        user = db.query(User).filter(User.username == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# Utility functions
def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_username(db,username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(email: str, db: Session = Depends(get_db)):
    return db.query(User).filter(User.email == email).first()
def hash_password(password: str):
    return pwd_context.hash(password)

def get_user_role_name(db: Session, user_id: int):
    # Query to get the role ID for the user
    role_id = db.query(user_roles.c.role_id).filter(user_roles.c.user_id == user_id).scalar()

    # Check if a role ID exists
    if not role_id:
        return None

    # Query to get the role name based on the role ID
    role_name = db.query(Role.name).filter(Role.id == role_id).scalar()

    return role_name