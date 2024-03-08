from src.config.database import db
from src.services.search_term.search_term_service import SearchTermService
from src.repositories.search_term import SearchTermRepository


async def get_search_term_service() -> SearchTermService:
    search_term_repository = SearchTermRepository(db, "search_terms")
    search_term_service = SearchTermService(
        search_term_repository=search_term_repository
    )
    return search_term_service
