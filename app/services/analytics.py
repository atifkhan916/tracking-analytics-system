from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from app.services.tracking import TrackingEventService
from app.services.marketing import MarketingTouchpointService

class AnalyticsService:
    def __init__(
        self,
        tracking_service: TrackingEventService,
        marketing_service: MarketingTouchpointService
    ):
        self.tracking_service = tracking_service
        self.marketing_service = marketing_service

    def get_user_analytics(
        self,
        *,
        user_id: str,
        start_time: datetime = None,
        end_time: datetime = None
    ) -> Dict[str, Any]:
        if not start_time:
            start_time = datetime.now(timezone.utc) - timedelta(days=30)
        if not end_time:
            end_time = datetime.now(timezone.utc)

        events = self.tracking_service.get_user_events(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time
        )

        touchpoints = self.marketing_service.get_user_touchpoints(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time
        )

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