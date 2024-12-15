from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class TrackingEventBase(BaseModel):
    user_id: str
    event_name: str
    amount: Optional[float] = None
    referral: Optional[str] = None
    url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class TrackingEventCreate(TrackingEventBase):
    pass

class TrackingEvent(TrackingEventBase):
    id: int
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class MarketingTouchpointBase(BaseModel):
    user_id: str
    event_name: str
    channel_name: str
    campaign_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MarketingTouchpointCreate(MarketingTouchpointBase):
    pass

class MarketingTouchpoint(MarketingTouchpointBase):
    id: int
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True