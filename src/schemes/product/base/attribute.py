from typing import Union, Optional
from pydantic import BaseModel, constr

from .attribute_values import Trivariate, Bivariate


class Attribute(BaseModel):
    """
    Represents a single attribute in the product.
    """
    code: constr(min_length=1)
    name: constr(min_length=1)
    value: Union[Trivariate, Bivariate, float, int, str]
    type: constr(min_length=1)
    unit: Optional[constr(min_length=1)] = None
    group: Optional[constr(min_length=1)] = None
    explanation: Optional[constr(min_length=1)] = None

