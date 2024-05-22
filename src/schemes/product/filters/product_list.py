from decimal import Decimal
from enum import Enum
from typing import Optional, Dict
from pydantic import condecimal, constr, Base64UrlStr, conint

from src.schemes.base.base_pagination_settings import BasePaginationSettings
from src.schemes.base.pyobject_id import PyObjectId
from src.dependencies.model_dependencies.facet_filters import get_facet_filters
from src.schemes.product.facet_values.facet_value_filters import FacetFilterObject


class ProductSortOptionsEnum(str, Enum):
    relevancy = "relevancy"  # The most relevant product first
    price_low_to_high = "price_low_to_high"  # Products with the lowest price first
    price_high_to_low = "price_high_to_low"  # Products with the highest price first
    ending_soonest = "ending_soonest"  # Products with the lowest stock goes first, but products with 0 stock goes last


class ProductFilters:
    """
    Class with parameters to filter product's facet values
    """

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
        # Validate chosen facets if they present, if not, set this field to None
        self.chosen_facets: Optional[Dict[str, FacetFilterObject]] = get_facet_filters(
            chosen_facets
        ) if chosen_facets is not None else None


class ProductPaginationSettings(BasePaginationSettings):
    def __init__(self,
                 page: conint(ge=0) = 1,
                 page_size: conint(ge=0) = 25,
                 sort_option: ProductSortOptionsEnum = ProductSortOptionsEnum.relevancy, ):
        super().__init__(page, page_size)
        self.sort_option = sort_option
