"""create task table

Revision ID: 09ef4d157dee
Revises: 99e261c94d89
Create Date: 2024-01-08 18:33:10.055447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "09ef4d157dee"
down_revision: Union[str, None] = "99e261c94d89"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("description", sa.Unicode(200)),
    )


def downgrade() -> None:
    op.drop_table("tasks")
