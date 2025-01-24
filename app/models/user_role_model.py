# user_role_model.py

from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base import Base  # Assuming your Base is defined in a separate file

# Association Table for Many-to-Many relationship between users and roles
user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True)
)
