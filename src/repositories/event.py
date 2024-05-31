from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase

from .base.base_repository import BaseRepository
from src.schemes.event.pagination_settings import EventPaginationSettings
from src.aggregation_pipelines.event.event_list import get_pipeline_to_retrieve_event_list


class EventRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, 'events')

    async def find_by_start_date_or_status(self, filters: dict, pagination_settings: EventPaginationSettings) -> Dict[str, Any]:
        """
        Returns all events which satisfy all passed conditions and count of gotten events.
        """
        pipeline = get_pipeline_to_retrieve_event_list(filters, pagination_settings)
        event_list = await self.db[self.collection_name].aggregate(pipeline).to_list(length=None)
        result = {
            'items': event_list[0].get('items') if event_list else [],
            'count': event_list[0].get('count') if event_list else 0,
        }
        return result



