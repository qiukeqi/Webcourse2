"""empty message

Revision ID: 7e6a5e00fd86
Revises: 6f0341b96cde
Create Date: 2020-12-29 01:24:14.792450

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7e6a5e00fd86'
down_revision = '6f0341b96cde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'date')
    op.create_unique_constraint(None, 'user', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.add_column('books', sa.Column('date', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###
