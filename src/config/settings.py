from typing import List

from pydantic import constr, confloat, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_url: constr(strip_whitespace=True)
    redis_cache_url: constr(strip_whitespace=True)
    atlas_search_product_index_name: constr(strip_whitespace=True) # A name of atlas search index to search products
    atlas_search_search_terms_index_name: constr(strip_whitespace=True) # A name of atlas search index
    # to filter search terms
    allowed_origins: List[constr(strip_whitespace=True)] = []
    relevance_threshold: confloat(ge=0, le=1) # Determines minimum relevance score of search item to be not excluded

settings = Settings()