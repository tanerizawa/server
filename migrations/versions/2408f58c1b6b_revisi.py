"""revisi

Revision ID: 2408f58c1b6b
Revises: da8b31e2805d
Create Date: 2025-06-27 21:16:02.411677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2408f58c1b6b'
down_revision: Union[str, Sequence[str], None] = 'da8b31e2805d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('emerging_themes', sa.JSON(), nullable=True, comment="Tema dominan dari jurnal & chat pengguna. Cth: {'pekerjaan': 0.8}"),
    sa.Column('sentiment_trend', sa.String(), nullable=True, comment="Tren sentimen pengguna. Cth: 'meningkat', 'menurun', 'stabil'"),
    sa.Column('last_analyzed', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_profiles_id'), 'user_profiles', ['id'], unique=False)
    op.create_index(op.f('ix_user_profiles_user_id'), 'user_profiles', ['user_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_profiles_user_id'), table_name='user_profiles')
    op.drop_index(op.f('ix_user_profiles_id'), table_name='user_profiles')
    op.drop_table('user_profiles')
    # ### end Alembic commands ###
