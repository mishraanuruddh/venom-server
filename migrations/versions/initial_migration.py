"""initial migration

Revision ID: initial
Revises: 
Create Date: 2024-01-04

"""
from alembic import op
import sqlalchemy as sa

revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('chat_id', sa.String(255), nullable=False),
        sa.Column('sender_id', sa.String(255), nullable=False),
        sa.Column('recipient_id', sa.String(255), nullable=False),
        sa.Column('message_type', sa.String(50), nullable=False),
        sa.Column('text_content', sa.Text),
        sa.Column('media_key', sa.String(255)),
        sa.Column('media_s3_path', sa.Text),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('deleted', sa.Boolean, default=False),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()')),
    )
    
    op.create_index('ix_messages_chat_id', 'messages', ['chat_id'])
    op.create_index('ix_messages_sender_id', 'messages', ['sender_id'])

def downgrade():
    op.drop_index('ix_messages_sender_id')
    op.drop_index('ix_messages_chat_id')
    op.drop_table('messages')