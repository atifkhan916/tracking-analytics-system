# alembic/versions/seed_initial_data.py
"""seed initial data

Revision ID: seed_initial_data
Revises: 1234567890ab
Create Date: 2023-12-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta
import random
import json

# revision identifiers, used by Alembic
revision = 'seed_initial_data'
down_revision = 'initial_db_setup'  # This should match your initial migration ID
branch_labels = None
depends_on = None

def upgrade() -> None:
    conn = op.get_bind()
    
    # Sample data
    user_ids = [f"user_{i}" for i in range(1, 6)]
    event_names = ["page_view", "add_to_cart", "purchase", "signup", "login"]
    urls = ["/products", "/cart", "/checkout", "/profile", "/homepage"]
    referrals = ["google", "facebook", "direct", "email", "twitter"]
    channels = ["facebook", "google", "linkedin", "email", "instagram"]
    campaign_ids = ["summer_sale_2023", "black_friday", "new_year_2024"]

    # Generate timestamps between last 30 days
    base_time = datetime.now() - timedelta(days=30)

    # Insert tracking events
    for i in range(20):
        timestamp = base_time + timedelta(hours=random.randint(0, 30*24))
        event_name = random.choice(event_names)
        amount = round(random.uniform(10.0, 500.0), 2) if event_name == "purchase" else None
        metadata = json.dumps({"session_id": f"sess_{i}", "device": random.choice(["mobile", "desktop"])})

        conn.execute(
            sa.text("""
                INSERT INTO tracking_events 
                (user_id, event_name, timestamp, amount, referral, url, event_metadata, created_at)
                VALUES 
                (:user_id, :event_name, :timestamp, :amount, :referral, :url, :event_metadata, :created_at)
            """),
            {
                "user_id": random.choice(user_ids),
                "event_name": event_name,
                "timestamp": timestamp,
                "amount": amount,
                "referral": random.choice(referrals),
                "url": random.choice(urls),
                "event_metadata": metadata,
                "created_at": datetime.now()
            }
        )

    # Insert marketing touchpoints
    for i in range(20):
        timestamp = base_time + timedelta(hours=random.randint(0, 30*24))
        metadata = json.dumps({"cost": random.randint(50, 500), "impressions": random.randint(1000, 5000)})

        conn.execute(
            sa.text("""
                INSERT INTO marketing_touchpoints 
                (user_id, event_name, channel_name, timestamp, campaign_id, event_metadata, created_at)
                VALUES 
                (:user_id, :event_name, :channel_name, :timestamp, :campaign_id, :event_metadata, :created_at)
            """),
            {
                "user_id": random.choice(user_ids),
                "event_name": random.choice(["impression", "click", "conversion"]),
                "channel_name": random.choice(channels),
                "timestamp": timestamp,
                "campaign_id": random.choice(campaign_ids),
                "event_metadata": metadata,
                "created_at": datetime.now()
            }
        )

def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM tracking_events"))
    conn.execute(sa.text("DELETE FROM marketing_touchpoints"))