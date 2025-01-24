# role_model.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models.base import Base  # Assuming your Base is defined in a separate file
from app.models.user_role_model import user_roles  # Import the user_roles association table

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)

    # Many-to-many relationship through user_roles association table
    users = relationship('User', secondary=user_roles, back_populates='roles')
