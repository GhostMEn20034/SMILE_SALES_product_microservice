from typing import Dict
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .base.base_repository import BaseRepository
from src.aggregation_pipelines.category.category_relations import get_category_relations


class CategoryRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, 'categories')

    async def get_category_ancestors_and_children(self, category_id: ObjectId, auto_defined: bool = False) -> Dict:
        """
        Returns category's ancestors and children
        :param category_id: ID of the category to get children and ancestors.
        :param auto_defined: Defines whether current category is defined automatically or specified manually.
        Required for response model further processing.
        """
        category = await self.db[self.collection_name].aggregate(
            pipeline=get_category_relations(category_id, self.collection_name, auto_defined)
        ).to_list(length=None)
        return category[0]
