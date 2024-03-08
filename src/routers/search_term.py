from typing import List, Annotated
from fastapi import APIRouter, Depends

from src.dependencies.service_dependencies.search_term import get_search_term_service
from src.services.search_term.search_term_service import SearchTermService
from src.schemes.search_term.get import SearchTermItem, SearchTermListFilters

router = APIRouter(
    prefix='/search'
)

ServiceDep = Annotated[SearchTermService, Depends(get_search_term_service)]
SearchTermParamsDep = Annotated[SearchTermListFilters, Depends(SearchTermListFilters)]

@router.get('/', response_model=List[SearchTermItem])
async def find_search_terms(filters: SearchTermParamsDep, service: ServiceDep):
    return await service.find_search_terms_by_name(filters.q)
