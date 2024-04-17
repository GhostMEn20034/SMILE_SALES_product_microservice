from typing import List, Optional
from bson import ObjectId

from src.schemes.facet.base import Facet

class ProductFacetParams:
    """
    Parameter class to encapsulate parameters for getting all products' facet values
    """
    def __init__(self, facets: List[Facet], category_ids: Optional[List[ObjectId]]):
        self.facets = facets
        self.category_ids = category_ids
