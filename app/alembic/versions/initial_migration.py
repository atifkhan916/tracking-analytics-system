#initial migration
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'initial_db_setup'
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