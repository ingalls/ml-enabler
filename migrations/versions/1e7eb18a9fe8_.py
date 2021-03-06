"""empty message

Revision ID: 1e7eb18a9fe8
Revises: 7abacee99e4d
Create Date: 2020-08-19 08:51:59.096778

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1e7eb18a9fe8'
down_revision = '7abacee99e4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('imagery', sa.Column('fmt', sa.String(), nullable=True))
    op.execute("UPDATE imagery SET fmt = 'wms'")
    op.alter_column('imagery', 'fmt', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('imagery', 'fmt')
    # ### end Alembic commands ###
