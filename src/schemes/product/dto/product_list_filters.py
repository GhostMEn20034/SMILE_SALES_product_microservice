from typing import Optional, Dict
from bson import ObjectId, Decimal128

from src.schemes.product.facet_values.facet_value_filters import FacetFilterObject

class ProductFiltersDto:
    def __init__(self,
                 min_price: Optional[Decimal128] = None,
                 max_price: Optional[Decimal128] = None,
                 category: Optional[ObjectId] = None,
                 q: Optional[str] = None,
                 chosen_facets: Optional[Dict[str, FacetFilterObject]] = None
                 ):
        self.min_price = min_price
        self.max_price = max_price
        self.category = category
        self.q = q
        self.chosen_facets = chosen_facets
