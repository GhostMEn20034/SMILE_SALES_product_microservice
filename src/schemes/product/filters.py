from decimal import Decimal
from typing import Any, Optional
from pydantic import BaseModel, condecimal, constr, Base64UrlStr

from src.schemes.base.pyobject_id import PyObjectId


class FacetFilterItem(BaseModel):
    code: constr(min_length=1)
    value: Any
    unit: Optional[constr(min_length=1)] = None


class ProductFilters:
    def __init__(self,
                 min_price: Optional[condecimal(ge=Decimal("0.00"), decimal_places=2)] = None,
                 max_price: Optional[condecimal(ge=Decimal("0.00"), decimal_places=2)] = None,
                 category: Optional[PyObjectId] = None,
                 q: Optional[constr(min_length=1, to_lower=True, strip_whitespace=True)] = None,
                 chosen_facets: Optional[Base64UrlStr] = None, ):
        self.min_price = min_price
        self.max_price = max_price
        self.category = category
        self.q = q
        self.chosen_facets = chosen_facets
