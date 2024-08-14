import fastapi
from typing import Annotated
from fastapi_cache.decorator import cache

from src.dependencies.service_dependencies.event import get_event_service
from src.schemes.base.pyobject_id import PyObjectId
from src.schemes.event.pagination_settings import EventPaginationSettings
from src.schemes.event.responses import EventListResponse, EventDetailsResponse
from src.services.event.event_service import EventService


router = fastapi.APIRouter(
    prefix="/events",
    tags=["Events"]
)


PaginationSettingsDep = Annotated[EventPaginationSettings, fastapi.Depends(EventPaginationSettings)]
ServiceDep = Annotated[EventService, fastapi.Depends(get_event_service)]


@router.get("/", response_model=EventListResponse)
@cache(expire=60 * 60, namespace="events") # Cache the response for 1 hour
async def get_event_list(service: ServiceDep, pagination_settings: PaginationSettingsDep) -> EventListResponse:
    return await service.get_active_and_recent_events(pagination_settings)


@router.get("/{event_id}", response_model=EventDetailsResponse)
@cache(expire=60 * 15, namespace="events") # Cache the response for 15 minutes
async def get_event_details(event_id: PyObjectId, service: ServiceDep) -> EventDetailsResponse:
    return await service.get_event_details(event_id)
