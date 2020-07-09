"""empty message

Revision ID: 2600f7a87583
Revises: 65b0dbc13dcb
Create Date: 2020-07-09 08:35:33.943105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2600f7a87583'
down_revision = '65b0dbc13dcb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('predictions', sa.Column('checkpoint_link', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('predictions', sa.Column('tfrecord_link', sa.TEXT(), autoincrement=False, nullable=True))


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('predictions', 'tfrecord_link')
    op.drop_column('predictions', 'checkpoint_link')
    # ### end Alembic commands ###
