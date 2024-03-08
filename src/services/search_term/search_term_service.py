from src.repositories.search_term import SearchTermRepository


class SearchTermService:
    def __init__(self, search_term_repository: SearchTermRepository):
        self.search_term_repository = search_term_repository

    async def find_search_terms_by_name(self, query: str):
        search_terms = await self.search_term_repository.find_search_terms_by_name(query)

        if len(query.strip()) > 0:
            await self.search_term_repository \
                .update_one_document({"name": query}, {"$inc": {"search_count": 1}})

        return search_terms