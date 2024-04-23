from pydantic import BaseModel, conint, Field

from src.schemes.base.pydecimal128 import PyDecimal128


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
