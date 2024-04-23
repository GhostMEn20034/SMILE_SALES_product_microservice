from typing import Optional, List, Union
from pydantic import BaseModel, constr

from src.schemes.product.base.attribute_values import Trivariate, Bivariate


class RangeFacetValue(BaseModel):
    gteq: Union[float, int] # Greater than equal
    ltn: Optional[Union[float, int]] = None # Less than


class FacetOption(BaseModel):
    """
    Represents a single facet option
    """
    value: Union[Trivariate, Bivariate, RangeFacetValue, float, int, str]
    unit: Optional[constr(min_length=1)] = None # unit of measurement


class FacetFilterObject(BaseModel):
    is_range: bool
    values: List[FacetOption]

