from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from . import models, schemas, database
from .config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Dependencies
get_db = database.get_db

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now(datetime.timezone.utc)}

@app.post("/tracking/events/", response_model=schemas.TrackingEvent)
def create_tracking_event(event: schemas.TrackingEventCreate, db: Session = Depends(get_db)):
    db_event = models.TrackingEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/tracking/events/", response_model=List[schemas.TrackingEvent])
def list_tracking_events(
    skip: int = 0,
    limit: int = 100,
    user_id: str = None,
    event_name: str = None,
    start_time: datetime = None,
    end_time: datetime = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.TrackingEvent)
    
    if user_id:
        query = query.filter(models.TrackingEvent.user_id == user_id)
    if event_name:
        query = query.filter(models.TrackingEvent.event_name == event_name)
    if start_time:
        query = query.filter(models.TrackingEvent.timestamp >= start_time)
    if end_time:
        query = query.filter(models.TrackingEvent.timestamp <= end_time)
    
    return query.order_by(models.TrackingEvent.timestamp.desc()).offset(skip).limit(limit).all()

@app.post("/marketing/touchpoints/", response_model=schemas.MarketingTouchpoint)
def create_marketing_touchpoint(touchpoint: schemas.MarketingTouchpointCreate, db: Session = Depends(get_db)):
    db_touchpoint = models.MarketingTouchpoint(**touchpoint.dict())
    db.add(db_touchpoint)
    db.commit()
    db.refresh(db_touchpoint)
    return db_touchpoint

@app.get("/marketing/touchpoints/", response_model=List[schemas.MarketingTouchpoint])
def list_marketing_touchpoints(
    skip: int = 0,
    limit: int = 100,
    user_id: str = None,
    channel_name: str = None,
    campaign_id: str = None,
    start_time: datetime = None,
    end_time: datetime = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.MarketingTouchpoint)
    
    if user_id:
        query = query.filter(models.MarketingTouchpoint.user_id == user_id)
    if channel_name:
        query = query.filter(models.MarketingTouchpoint.channel_name == channel_name)
    if campaign_id:
        query = query.filter(models.MarketingTouchpoint.campaign_id == campaign_id)
    if start_time:
        query = query.filter(models.MarketingTouchpoint.timestamp >= start_time)
    if end_time:
        query = query.filter(models.MarketingTouchpoint.timestamp <= end_time)
    
    return query.order_by(models.MarketingTouchpoint.timestamp.desc()).offset(skip).limit(limit).all()

@app.get("/analytics/user/{user_id}")
def get_user_analytics(
    user_id: str,
    start_time: datetime = None,
    end_time: datetime = None,
    db: Session = Depends(get_db)
):
    if not start_time:
        start_time = datetime.utcnow() - timedelta(days=30)
    if not end_time:
        end_time = datetime.utcnow()

    # Get tracking events
    events = db.query(models.TrackingEvent)\
        .filter(
            models.TrackingEvent.user_id == user_id,
            models.TrackingEvent.timestamp.between(start_time, end_time)
        )\
        .all()

    # Get marketing touchpoints
    touchpoints = db.query(models.MarketingTouchpoint)\
        .filter(
            models.MarketingTouchpoint.user_id == user_id,
            models.MarketingTouchpoint.timestamp.between(start_time, end_time)
        )\
        .all()

    return {
        "user_id": user_id,
        "period": {
            "start": start_time,
            "end": end_time
        },
        "events": {
            "total_count": len(events),
            "events": events
        },
        "marketing": {
            "total_touchpoints": len(touchpoints),
            "touchpoints": touchpoints
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)