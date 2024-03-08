from motor.motor_asyncio import AsyncIOMotorDatabase

from .base.base_repository import BaseRepository
from src.aggregation_pipelines.search_term.search_term_list import (
    get_pipeline_to_find_search_terms,
    get_pipeline_to_find_top_n_search_terms
)


class SearchTermRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        super().__init__(db, collection_name)
        self.search_term_collection = collection_name

    async def find_search_terms_by_name(self, query: str):
        if len(query.strip()) == 0:
            pipeline = get_pipeline_to_find_top_n_search_terms()
            search_terms_list = await self.db[self.search_term_collection].aggregate(pipeline=pipeline).to_list(
                length=None)
            return search_terms_list

        pipeline = get_pipeline_to_find_search_terms(query)
        search_terms_list = await self.db[self.search_term_collection].aggregate(pipeline=pipeline).to_list(length=None)
        return search_terms_list
