"""empty message

Revision ID: 2974dcf09043
Revises: a60216f4b445
Create Date: 2021-05-27 21:25:36.431402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2974dcf09043'
down_revision = 'a60216f4b445'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feedback', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feedback', 'description')
    # ### end Alembic commands ###