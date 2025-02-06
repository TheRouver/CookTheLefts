"""Add unique constraint to comments

Revision ID: 95148f344d4d
Revises: e775e04cc680
Create Date: 2025-01-12 17:04:25.265107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95148f344d4d'
down_revision = 'e775e04cc680'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_user_recipe_comment', ['user_id', 'recipe_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint('unique_user_recipe_comment', type_='unique')

    # ### end Alembic commands ###
