from typing import List, Optional

from bson import ObjectId


class ProductFacetParams:
    """
    Parameter class to encapsulate parameters for getting all products' facet values
    """
    def __init__(self, facet_codes: List[str], category_ids: Optional[List[ObjectId]]):
        self.facet_codes = facet_codes
        self.category_ids = category_ids
