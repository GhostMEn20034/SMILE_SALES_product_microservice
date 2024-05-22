from typing import Dict, Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .base.base_repository import BaseRepository
from src.schemes.deal.pagination_settings import DealPaginationSettings
from src.aggregation_pipelines.deal.deal_list import get_pipeline_to_retrieve_list_of_deals
from src.aggregation_pipelines.deal.parent_deal_details import get_pipeline_to_retrieve_parent_deal_details
from src.param_classes.deal.parent_deal_details import ParentDealDetailsParams


class DealRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, 'deals')

    async def get_list_of_visible_deals(self, pagination_settings: DealPaginationSettings) -> Dict[str, Any]:
        """
        Returns all visible deal which have is_parent True OR parent_id None (null)
        """
        pipeline = get_pipeline_to_retrieve_list_of_deals(pagination_settings)
        result = await self.db[self.collection_name].aggregate(pipeline).to_list(length=None)
        formatted_result = {
            'items': result[0].get('items') if result[0] else [],
            'count': result[0].get('count') if result[0] else 0,
        }
        return formatted_result

    async def get_parent_deal_by_id(self, deal_id: ObjectId) -> Dict[str, Any]:
        parent_deal_details_params = ParentDealDetailsParams(deal_id=deal_id, collection_name=self.collection_name)
        pipeline = get_pipeline_to_retrieve_parent_deal_details(parent_deal_details_params)

        result = await self.db[self.collection_name].aggregate(pipeline).to_list(length=None)
        return result[0] if result[0] else {}
