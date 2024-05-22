import fastapi
from typing import Annotated

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
async def get_deal_list(pagination_settings: PaginationSettingsDep, service: ServiceDep):
    return await service.get_visible_deals(pagination_settings)


@router.get("/{deal_id}", response_model=DealDetailsResponse)
async def get_deal_details(deal_id: PyObjectId, service: ServiceDep):
    return await service.get_parent_deal_details(deal_id)
