"""init

Revision ID: 6cf2ea1fa884
Revises: 
Create Date: 2023-10-12 18:07:50.203571

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey


# revision identifiers, used by Alembic.
revision = '6cf2ea1fa884'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        Column("id", Integer, primary_key=True),
        Column("email", String, unique=True, index=True),
        Column("hashed_password", String),
        Column("is_active", Boolean, default=True),
    )

    op.create_table(
        "todo",
        Column("id", Integer, primary_key=True, index=True),
        Column("title", String, nullable=False),
        Column("description", String),
        Column("priority", Integer, nullable=False),
        Column("complete", Boolean, default=False),
        Column("user_id", Integer, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('todo')
    op.drop_table('user')
