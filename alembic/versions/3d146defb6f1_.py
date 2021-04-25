"""

Revision ID: 3d146defb6f1
Revises: 1e208eb360bd
Create Date: 2021-04-25 16:35:58.121123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d146defb6f1'
down_revision = '1e208eb360bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photos', sa.Column('event_id', sa.Integer(), nullable=True))
    op.drop_constraint('photos_parent_id_fkey', 'photos', type_='foreignkey')
    op.create_foreign_key(None, 'photos', 'events', ['event_id'], ['id'])
    op.drop_column('photos', 'parent_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photos', sa.Column('parent_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'photos', type_='foreignkey')
    op.create_foreign_key('photos_parent_id_fkey', 'photos', 'events', ['parent_id'], ['id'])
    op.drop_column('photos', 'event_id')
    # ### end Alembic commands ###