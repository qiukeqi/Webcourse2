"""empty message

Revision ID: 829fa62a4af4
Revises: 7e6a5e00fd86
Create Date: 2020-12-31 17:12:07.045106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '829fa62a4af4'
down_revision = '7e6a5e00fd86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('lastLoginTime', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'lastLoginTime')
    # ### end Alembic commands ###
