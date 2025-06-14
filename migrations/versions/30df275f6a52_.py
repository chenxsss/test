"""empty message

Revision ID: 30df275f6a52
Revises: 0d0e0ec31422
Create Date: 2025-06-12 17:20:12.623201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30df275f6a52'
down_revision = '0d0e0ec31422'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_time', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('create_time')

    # ### end Alembic commands ###
