from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .base.base_repository import BaseRepository
from src.aggregation_pipelines.facet.category_priority import get_pipeline_to_retrieve_facets_by_category_priority


class FacetRepository(BaseRepository):

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, 'facets')

    async def get_facet_codes_by_category_priority(self, category_ids: List[ObjectId], include_common_facets = True, limit: int = 40):
        """
        This method queries the 'facets' collection and returns a list of facet codes.
        Each facet is associated with one or more categories, and the facets are returned
        in order of priority based on the category they are associated with. The priority
        is determined by the order of category IDs provided in the 'category_ids' list,
        with the first ID having the highest priority.

        :param category_ids: List of category identifiers.
        :param include_common_facets: A flag that indicates the inclusion of facets belonging to all categories
        :param limit: Maximum number of facets in result
        """
        # Include facets belonging to all categories if include_common_facets is True
        category_ids = category_ids if not include_common_facets else ["*", *category_ids]
        pipeline = get_pipeline_to_retrieve_facets_by_category_priority(category_ids, limit)
        facets = await self.db[self.collection_name].aggregate(pipeline=pipeline).to_list(length=None)
        return facets
