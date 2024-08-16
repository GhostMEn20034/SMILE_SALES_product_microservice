from motor.motor_asyncio import AsyncIOMotorDatabase

from .base.base_repository import BaseRepository
from src.aggregation_pipelines.search_term.search_term_list import (
    get_pipeline_to_find_search_terms,
    get_pipeline_to_find_top_n_search_terms
)


class SearchTermRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, 'search_terms')

    async def find_search_terms_by_name(self, query: str):
        pipeline = get_pipeline_to_find_search_terms(query)
        search_terms_list = await self.db[self.collection_name].aggregate(pipeline=pipeline).to_list(length=None)
        return search_terms_list

    async def get_the_most_popular_search_terms(self):
        """
        Return top 10 the most popular search terms.
        """
        pipeline = get_pipeline_to_find_top_n_search_terms()
        search_terms_list = await self.db[self.collection_name].aggregate(pipeline=pipeline).to_list(
            length=None)
        return search_terms_list
