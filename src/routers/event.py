import fastapi
from typing import Annotated

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
async def get_event_list(service: ServiceDep, pagination_settings: PaginationSettingsDep):
    return await service.get_active_and_recent_events(pagination_settings)


@router.get("/{event_id}", response_model=EventDetailsResponse)
async def get_event_details(event_id: PyObjectId, service: ServiceDep):
    return await service.get_event_details(event_id)
