from datetime import datetime
from typing import List, Optional
from app.repositories.tracking import TrackingEventRepository
from app.schemas import TrackingEventCreate, TrackingEvent
from .base import BaseService

class TrackingEventService(BaseService[TrackingEvent, TrackingEventCreate, TrackingEventCreate]):
    def __init__(self, repository: TrackingEventRepository):
        super().__init__(repository)
        self.repository = repository

    def get_user_events(
        self,
        *,
        user_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[TrackingEvent]:
        return self.repository.get_events_by_timeframe(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time
        )
