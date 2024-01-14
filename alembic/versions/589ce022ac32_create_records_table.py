"""create records table

Revision ID: 589ce022ac32
Revises: 09ef4d157dee
Create Date: 2024-01-09 08:52:19.433300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "589ce022ac32"
down_revision: Union[str, None] = "09ef4d157dee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "records",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("content", sa.Unicode(200), nullable=False),
        sa.Column("task_id", sa.UUID, nullable=False, index=True),
        sa.ForeignKeyConstraint(
            ("task_id",),
            ["tasks.id"],
        ),
    )


def downgrade() -> None:
    op.drop_table("records")
