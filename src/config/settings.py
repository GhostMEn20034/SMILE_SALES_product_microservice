from typing import List
from pydantic_settings import BaseSettings
from pydantic import MongoDsn

class Settings(BaseSettings):
    mongodb_url: MongoDsn
    atlas_search_product_index_name: str
    atlas_search_search_terms_index_name: str
    allowed_origins: List[str]


settings = Settings()