"""empty message

Revision ID: e41d6ecc6176
Revises: 
Create Date: 2021-06-02 11:54:16.864922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e41d6ecc6176'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('topic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('hot', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('user_avatar', sa.String(length=1024), nullable=True),
    sa.Column('user_name', sa.String(length=256), nullable=True),
    sa.Column('publish_time', sa.DateTime(), nullable=True),
    sa.Column('forward_count', sa.Integer(), nullable=True),
    sa.Column('comment_count', sa.Integer(), nullable=True),
    sa.Column('like_count', sa.Integer(), nullable=True),
    sa.Column('image_list', sa.JSON(), nullable=True),
    sa.Column('vedio_list', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feed_id', sa.Integer(), nullable=True),
    sa.Column('user_avatar', sa.String(length=1024), nullable=True),
    sa.Column('user_name', sa.String(length=256), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('image', sa.String(length=1024), nullable=True),
    sa.Column('publish_time', sa.DateTime(), nullable=True),
    sa.Column('like_count', sa.Integer(), nullable=True),
    sa.Column('reply_name', sa.String(length=256), nullable=True),
    sa.Column('reply_content', sa.Text(), nullable=True),
    sa.Column('reply_time', sa.DateTime(), nullable=True),
    sa.Column('reply_like', sa.Integer(), nullable=True),
    sa.Column('reply_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('feed')
    op.drop_table('topic')
    # ### end Alembic commands ###