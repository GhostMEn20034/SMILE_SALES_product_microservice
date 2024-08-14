import fastapi
from typing import Annotated
from fastapi_cache.decorator import cache

from src.schemes.base.pyobject_id import PyObjectId
from src.services.deal.deal_service import DealService
from src.schemes.deal.pagination_settings import DealPaginationSettings
from src.schemes.deal.responses import DealListResponse, DealDetailsResponse
from src.dependencies.service_dependencies.deal import get_deal_service

router = fastapi.APIRouter(
    prefix="/deals",
    tags=["Deals"]
)


PaginationSettingsDep = Annotated[DealPaginationSettings, fastapi.Depends(DealPaginationSettings)]
ServiceDep = Annotated[DealService, fastapi.Depends(get_deal_service)]


@router.get("/", response_model=DealListResponse)
@cache(expire=60 * 60, namespace="deals") # Cache the response for 1 hour
async def get_deal_list(pagination_settings: PaginationSettingsDep, service: ServiceDep) -> DealListResponse:
    return await service.get_visible_deals(pagination_settings)


@router.get("/{deal_id}", response_model=DealDetailsResponse)
@cache(expire=60 * 15, namespace="deals") # Cache the response for 15 minutes
async def get_deal_details(deal_id: PyObjectId, service: ServiceDep) -> DealDetailsResponse:
    return await service.get_parent_deal_details(deal_id)
