from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TrackingEvent(Base):
    __tablename__ = "tracking_events"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    event_name = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.now(datetime.timezone.utc), index=True)
    amount = Column(Float)
    referral = Column(String)
    url = Column(Text)
    event_metadata = Column(JSON)  # Changed from metadata to event_metadata
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc))

class MarketingTouchpoint(Base):
    __tablename__ = "marketing_touchpoints"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    event_name = Column(String, nullable=False, index=True)
    channel_name = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.now(datetime.timezone.utc), index=True)
    campaign_id = Column(String, index=True)
    event_metadata = Column(JSON)  # Changed from metadata to event_metadata
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc))