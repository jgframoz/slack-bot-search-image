"""workspace in QueryMetric

Revision ID: d8cc52386845
Revises: 149ead18efba
Create Date: 2022-08-18 08:53:39.535386

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd8cc52386845'
down_revision = '149ead18efba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('query_metrics', sa.Column('workspace', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('query_metrics', 'workspace')
    # ### end Alembic commands ###
