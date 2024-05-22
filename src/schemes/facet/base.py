from typing import Optional, List, Any, Union

from bson import ObjectId
from pydantic import BaseModel, Field, constr, field_validator

from src.schemes.base.pyobject_id import PyObjectId

class RangeValue(BaseModel):
    """
    Represents range of first number (gteq) inclusive and the second number (ltn) exclusive
    """
    gteq: Union[float, int] # Greater than equal value
    ltn: Optional[Union[float, int]] = None # Less than value
    display_name: constr(min_length=1) # Display Name - string representation of
    # range of gteq inclusive and ltn exclusive

    @field_validator('gteq', 'ltn', mode='before')
    @classmethod
    def preserve_type(cls, v):
        if v is None:
            return v

        if isinstance(v, float) and v.is_integer():
            return int(v)

        return v


class Facet(BaseModel):
    id: PyObjectId = Field(alias="_id")
    code: str
    name: str
    type: str
    optional: bool
    show_in_filters: bool
    values: Optional[List[Any]] = None
    categories: Union[List[PyObjectId], str]
    units: Optional[List[str]] = None
    is_range: bool = False
    range_values: Optional[List[RangeValue]] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}