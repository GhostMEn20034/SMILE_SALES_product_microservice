from typing import Any, Optional, List
from pydantic import BaseModel, constr, conint, Field, AnyHttpUrl

from src.schemes.base.pydecimal128 import PyDecimal128
from src.schemes.base.pyobject_id import PyObjectId


class FacetValueItem(BaseModel):
    """
    Represents a single value item within a facet.
    This model captures the details of a facet value, including its unit, count, and display name.
    """
    # The actual value of the facet item.
    value: Any
    # The unit of measurement for the facet value, if applicable.
    unit: Optional[constr(min_length=1)] = None
    # The number of occurrences or frequency of the facet value.
    count: conint(ge=0)
    # The human-readable name for the facet value.
    display_name: constr(min_length=1)


class FacetValuesObject(BaseModel):
    """
    Encapsulates the values associated with a specific facet code and name.

    This model is used to store and transmit the collection of values that belong to a particular facet,
    along with an explanation for the facet.
    """
    # The unique code identifier for the facet.
    code: constr(min_length=1)
    # The human-readable name of the facet.
    name: constr(min_length=1)
    # A brief description or explanation of the facet.
    explanation: Optional[constr(min_length=1)]
    # A list of `FacetValueItem` instances representing the facet's values.
    values: List[FacetValueItem]


class PriceRange(BaseModel):
    """
    Represents a range of prices with minimum and maximum boundaries.
    This model is used to define a price interval, which can be utilized in filtering products
    within a specified price range.
    """
    min: PyDecimal128
    max: PyDecimal128


class PriceRangeFacet(BaseModel):
    """
    Associates a price range with a count of items that fall within that range.

    This model is particularly useful for representing a facet of price ranges,
    where each range is associated with a number of products that are priced within it.
    """
    # The price range object, aliased as '_id' to match database conventions.
    id: PriceRange = Field(alias="_id")
    # The count of items within the specified price range.
    count: conint(ge=0)


class ProductListItem(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: constr(min_length=1)
    discounted_price: PyDecimal128 = Field()
    original_price: PyDecimal128 = Field()
    discount_percentage: Optional[PyDecimal128] = Field(default=None)
    stock: conint(ge=0)
    max_order_qty: conint(ge=0)
    image: AnyHttpUrl
