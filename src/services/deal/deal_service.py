from fastapi import HTTPException, status
from math import ceil
from typing import Dict, Any
from bson import ObjectId

from src.repositories.deal import DealRepository
from src.schemes.deal.base import Deal, DealDetails
from src.schemes.deal.pagination_settings import DealPaginationSettings
from src.schemes.deal.responses import DealListResponse, DealDetailsResponse


class DealService:
    def __init__(self, deal_repository: DealRepository):
        self.deal_repository = deal_repository

    async def get_visible_deals(self, pagination_settings: DealPaginationSettings) -> DealListResponse:
        result: Dict[str, Any] = await self.deal_repository.get_list_of_visible_deals(pagination_settings)
        result["page_count"]: int = ceil(result["count"] / pagination_settings.page_size)
        return DealListResponse(**result)

    async def get_parent_deal_details(self, deal_id: ObjectId) -> DealDetailsResponse:
        is_deal_exists: bool = await self.deal_repository.is_document_exists({"_id": deal_id,
                                                                        "is_visible": True,
                                                                        "is_parent": True})
        if not is_deal_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="The deal with the specified criteria does not exist")

        deal: Dict[str, Any] = await self.deal_repository.get_parent_deal_by_id(deal_id)
        validated_deal: Deal = DealDetails(**deal)
        return DealDetailsResponse(item=validated_deal, children=deal.get("children", []))
