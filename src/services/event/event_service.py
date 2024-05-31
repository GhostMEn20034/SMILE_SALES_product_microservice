from fastapi import HTTPException
from math import ceil
from datetime import datetime, timedelta
from typing import Dict, Any
from bson import ObjectId

from src.repositories.event import EventRepository
from src.repositories.product import ProductRepository
from src.schemes.event.base import EventStatusEnum
from src.schemes.event.pagination_settings import EventPaginationSettings
from src.schemes.event.responses import EventListResponse, EventDetailsResponse


class EventService:
    def __init__(self, event_repository: EventRepository, product_repository: ProductRepository):
        self.event_repository = event_repository
        self.product_repository = product_repository

    async def get_active_and_recent_events(self, pagination_settings: EventPaginationSettings) -> EventListResponse:

        # Filter events by start date current date minus 5 days and status in "created", "started"
        result: Dict[str, Any] = await self.event_repository.find_by_start_date_or_status(
            {"status": "started"}, pagination_settings
        )
        result["page_count"]: int = ceil(result["count"] / pagination_settings.page_size)
        return EventListResponse(**result)

    async def get_event_details(self, event_id: ObjectId) -> EventDetailsResponse:
        event_data = await self.event_repository.get_one_document(
            {"_id": event_id},
            {"discounted_products": 0},
        )
        if not event_data:
            raise HTTPException(status_code=404, detail="Event not found")

        product_count_by_category = await self.product_repository.get_product_count_by_category_with_join(
            {"event_id": event_id},
        ) if event_data["status"] != EventStatusEnum.ended.value else None

        return EventDetailsResponse(
            item=event_data,
            product_count_by_category=product_count_by_category
        )

