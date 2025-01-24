# user_model.py

from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.models.base import Base  # Assuming your Base is defined in a separate file
from app.models.user_role_model import user_roles  # Import the user_roles association table

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    # Many-to-many relationship through user_roles association table
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    tasks = relationship('Task', back_populates='user', cascade='all, delete-orphan')