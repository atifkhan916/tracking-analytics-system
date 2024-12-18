from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import TrackingEvent
from .base import BaseRepository

class TrackingEventRepository(BaseRepository[TrackingEvent]):
    def get_events_by_timeframe(
        self,
        *,
        user_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[TrackingEvent]:
        return (
            self.db.query(self.model)
            .filter(
                self.model.user_id == user_id,
                self.model.timestamp.between(start_time, end_time)
            )
            .order_by(self.model.timestamp.desc())
            .all()
        )