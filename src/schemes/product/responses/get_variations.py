from typing import List, Dict, Union, Optional
from pydantic import BaseModel, Field, constr

from src.schemes.base.pyobject_id import PyObjectId
from src.schemes.category.base import CategoryShortInfo
from src.schemes.product.base.attribute_values import Trivariate, Bivariate


class VariationsAttribute(BaseModel):
    """
    Represents an attribute of a variation with a value and an optional unit.
    """
    value: Union[Trivariate, Bivariate, float, int, str]
    unit: Optional[constr(min_length=1)] = None


class OptionChoice(BaseModel):
    """
    Represents a choice option in the choice list,
    containing values and a display name (user-friendly representation of the choice's values).
    """
    values: Dict[str, VariationsAttribute]
    display_name: str


class VariationOption(BaseModel):
    """
    Represents a variation option.
    """
    option_name: constr(min_length=1)
    attribute_codes: List[constr(min_length=1)]
    choices: List[OptionChoice]


class ProductVariationListItem(BaseModel):
    """
    Represents an item of product variation list.
    """
    id: PyObjectId = Field(alias="_id")
    name: constr(min_length=1)
    variation_attributes: Dict[str, VariationsAttribute]


class VariationSummary(BaseModel):
    """
    Represents summary information about variations.
    """
    variation_count: int = 0
    variation_options: List[VariationOption]


class GetVariationsResponse(BaseModel):
    items: List[ProductVariationListItem]
    variation_summary: VariationSummary
    category_hierarchy: List[CategoryShortInfo]

