from datetime import datetime
from typing import List, Optional
from app.repositories.marketing import MarketingTouchpointRepository
from app.schemas import MarketingTouchpointCreate, MarketingTouchpoint
from .base import BaseService

class MarketingTouchpointService(BaseService[MarketingTouchpoint, MarketingTouchpointCreate, MarketingTouchpointCreate]):
    def __init__(self, repository: MarketingTouchpointRepository):
        super().__init__(repository)
        self.repository = repository

    def get_user_touchpoints(
        self,
        *,
        user_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[MarketingTouchpoint]:
        return self.repository.get_touchpoints_by_timeframe(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time
        )