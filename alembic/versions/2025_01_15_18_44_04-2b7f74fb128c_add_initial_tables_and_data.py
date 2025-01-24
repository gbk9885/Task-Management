"""Add initial tables and data

Revision ID: 2b7f74fb128c
Revises: c153ef9f5e73
Create Date: 2025-01-15 18:44:04.604887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2b7f74fb128c'
down_revision: Union[str, None] = 'c153ef9f5e73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



# Insert records into tables
def upgrade():
    # Insert roles
    op.execute("""
        INSERT INTO roles (id, name, description)
        VALUES
        (1, 'Admin', 'Administrator role with all permissions'),
        (2, 'Manager', 'Manager role with content management permissions'),
        (3, 'User', 'User role with read-only access')
    """)

def downgrade():
    op.execute("DELETE FROM tasks WHERE id BETWEEN 1 AND 10")
    op.execute("DELETE FROM user_roles WHERE user_id BETWEEN 1 AND 10")
    op.execute("DELETE FROM roles WHERE id BETWEEN 1 AND 3")
    op.execute("DELETE FROM users WHERE id BETWEEN 1 AND 10")
