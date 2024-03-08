from typing import Optional, List
from pydantic import BaseModel, constr


class SearchTermItem(BaseModel):
    name: constr(min_length=1, to_lower=True, strip_whitespace=True)
    trend_search_term: bool

class SearchTermListFilters(BaseModel):
    q: Optional[constr(strip_whitespace=True, to_lower=True)] = ''
