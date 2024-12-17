from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from app import models, schemas
from app.database import get_db
from app.config import settings
from app.repositories.tracking import TrackingEventRepository
from app.repositories.marketing import MarketingTouchpointRepository
from app.services.tracking import TrackingEventService
from app.services.marketing import MarketingTouchpointService
from app.services.analytics import AnalyticsService

app = FastAPI(title=settings.PROJECT_NAME)

# Dependencies
def get_tracking_service(db: Session = Depends(get_db)) -> TrackingEventService:
    repository = TrackingEventRepository(models.TrackingEvent, db)
    return TrackingEventService(repository)

def get_marketing_service(db: Session = Depends(get_db)) -> MarketingTouchpointService:
    repository = MarketingTouchpointRepository(models.MarketingTouchpoint, db)
    return MarketingTouchpointService(repository)

def get_analytics_service(
    tracking_service: TrackingEventService = Depends(get_tracking_service),
    marketing_service: MarketingTouchpointService = Depends(get_marketing_service)
) -> AnalyticsService:
    return AnalyticsService(tracking_service, marketing_service)

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}

@app.post("/tracking/events/", response_model=schemas.TrackingEvent)
def create_tracking_event(
    event: schemas.TrackingEventCreate,
    service: TrackingEventService = Depends(get_tracking_service)
):
    return service.create(obj_in=event)

@app.get("/tracking/events/", response_model=List[schemas.TrackingEvent])
def list_tracking_events(
    skip: int = 0,
    limit: int = 30,
    user_id: str = None,
    event_name: str = None,
    start_time: datetime = None,
    end_time: datetime = None,
    service: TrackingEventService = Depends(get_tracking_service)
):
    filters = {
        "user_id": user_id,
        "event_name": event_name,
        "start_time": start_time,
        "end_time": end_time
    }
    return service.get_multi(skip=skip, limit=limit, **filters)

@app.post("/marketing/touchpoints/", response_model=schemas.MarketingTouchpoint)
def create_marketing_touchpoint(
    touchpoint: schemas.MarketingTouchpointCreate,
    service: MarketingTouchpointService = Depends(get_marketing_service)
):
    return service.create(obj_in=touchpoint)

@app.get("/marketing/touchpoints/", response_model=List[schemas.MarketingTouchpoint])
def list_marketing_touchpoints(
    skip: int = 0,
    limit: int = 30,
    user_id: str = None,
    channel_name: str = None,
    campaign_id: str = None,
    start_time: datetime = None,
    end_time: datetime = None,
    service: MarketingTouchpointService = Depends(get_marketing_service)
):
    filters = {
        "user_id": user_id,
        "channel_name": channel_name,
        "campaign_id": campaign_id,
        "start_time": start_time,
        "end_time": end_time
    }
    return service.get_multi(skip=skip, limit=limit, **filters)

@app.get("/analytics/user/{user_id}")
def get_user_analytics(
    user_id: str,
    start_time: datetime = None,
    end_time: datetime = None,
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_user_analytics(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)