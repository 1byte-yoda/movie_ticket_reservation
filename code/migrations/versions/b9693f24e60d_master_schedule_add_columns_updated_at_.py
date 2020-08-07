"""master_schedule ADD COLUMNS updated_at created_at

Revision ID: b9693f24e60d
Revises: 854029f35bfa
Create Date: 2020-08-07 15:05:41.963980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9693f24e60d'
down_revision = '854029f35bfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('master_schedule', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('master_schedule', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('master_schedule', 'updated_at')
    op.drop_column('master_schedule', 'created_at')
    # ### end Alembic commands ###
