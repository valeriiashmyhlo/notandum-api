"""Task add total records and labels

Revision ID: b93bf24c06ff
Revises: cec5ac1d0494
Create Date: 2024-02-01 08:42:00.101781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b93bf24c06ff'
down_revision: Union[str, None] = 'cec5ac1d0494'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('total_records', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('total_labels', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_tasks_total_labels'), 'tasks', ['total_labels'], unique=False)
    op.create_index(op.f('ix_tasks_total_records'), 'tasks', ['total_records'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tasks_total_records'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_total_labels'), table_name='tasks')
    op.drop_column('tasks', 'total_labels')
    op.drop_column('tasks', 'total_records')
    # ### end Alembic commands ###
