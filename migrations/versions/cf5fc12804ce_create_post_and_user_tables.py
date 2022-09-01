"""create Post and User tables

Revision ID: cf5fc12804ce
Revises: 
Create Date: 2022-08-29 15:42:12.290920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf5fc12804ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author', sa.String(), server_default='ismail', nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=200), nullable=True),
    sa.Column('last_name', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('password', sa.Text(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('is_superuser', sa.Boolean(), server_default='f', nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('posts')
    # ### end Alembic commands ###
