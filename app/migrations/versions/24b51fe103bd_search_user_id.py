"""search user id

Revision ID: 24b51fe103bd
Revises: 1f19fc3f8361
Create Date: 2022-09-04 23:23:36.292424

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '24b51fe103bd'
down_revision = '1f19fc3f8361'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images_metadata', sa.Column('user_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('images_metadata', 'user_id')
    # ### end Alembic commands ###