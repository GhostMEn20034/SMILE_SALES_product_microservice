from src.repositories.search_term import SearchTermRepository


class SearchTermService:
    def __init__(self, search_term_repository: SearchTermRepository):
        self.search_term_repository = search_term_repository

    async def find_search_terms_by_name(self, query: str):
        search_terms = await self.search_term_repository.find_search_terms_by_name(query)
        return search_terms

    async def increment_searched_count(self, search_term: str):
        """
        Increment the search term's "search_count" field by 1
        """
        if search_term.strip():
            await self.search_term_repository.update_one_document({"name": search_term.strip()},
                                                                  {"$inc": {"search_count": 1}})

