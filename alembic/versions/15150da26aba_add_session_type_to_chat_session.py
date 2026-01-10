"""add session type to chat session

Revision ID: 15150da26aba
Revises: 8e34acdfe057
Create Date: 2026-01-09 04:41:12.833234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15150da26aba'
down_revision: Union[str, None] = '8e34acdfe057'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE sessiontype AS ENUM ('CHAT', 'VIDEO')")
    
    op.add_column('chatsession', sa.Column('session_type', sa.Enum('CHAT', 'VIDEO', name='sessiontype', create_type=False), nullable=False, server_default='CHAT'))


def downgrade() -> None:
    op.drop_column('chatsession', 'session_type')
    op.execute("DROP TYPE IF EXISTS sessiontype")
