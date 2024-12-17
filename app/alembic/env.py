import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Get the absolute path of the directory containing env.py
current_path = os.path.dirname(os.path.abspath(__file__))
# Get the root path (app directory)
root_path = os.path.dirname(current_path)

# Add root path to Python path
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from models import Base
from config import settings

#from app.models import Base
#from app.config import settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    return settings.DATABASE_URL

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# app/alembic/versions/initial_migration.py
"""initial migration

Revision ID: 1234567890ab
Revises: 
Create Date: 2023-12-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '1234567890ab'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'tracking_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('event_name', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.Column('referral', sa.String(), nullable=True),
        sa.Column('url', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tracking_events_user_id', 'tracking_events', ['user_id'])
    op.create_index('ix_tracking_events_event_name', 'tracking_events', ['event_name'])
    op.create_index('ix_tracking_events_timestamp', 'tracking_events', ['timestamp'])

    op.create_table(
        'marketing_touchpoints',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('event_name', sa.String(), nullable=False),
        sa.Column('channel_name', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('campaign_id', sa.String(), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_marketing_touchpoints_user_id', 'marketing_touchpoints', ['user_id'])
    op.create_index('ix_marketing_touchpoints_channel_name', 'marketing_touchpoints', ['channel_name'])
    op.create_index('ix_marketing_touchpoints_campaign_id', 'marketing_touchpoints', ['campaign_id'])
    op.create_index('ix_marketing_touchpoints_timestamp', 'marketing_touchpoints', ['timestamp'])

def downgrade() -> None:
    op.drop_table('marketing_touchpoints')
    op.drop_table('tracking_events')