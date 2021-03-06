"""empty message

Revision ID: 69f682394874
Revises: 18ffda92762f
Create Date: 2020-08-10 11:19:52.923443

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '69f682394874'
down_revision = '18ffda92762f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('integration',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('model_id', sa.BigInteger(), nullable=False),
        sa.Column('integration', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['model_id'], ['ml_models.id'], name='fk_models'),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('integration')
    # ### end Alembic commands ###
