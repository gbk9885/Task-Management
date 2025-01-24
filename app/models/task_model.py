# task_model.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.models.base import Base  # Assuming your Base is defined in a separate file

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(String(20), nullable=False, server_default='pending')
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    # Use string-based reference for 'User' to avoid circular import issues
    user = relationship('User', back_populates='tasks')
