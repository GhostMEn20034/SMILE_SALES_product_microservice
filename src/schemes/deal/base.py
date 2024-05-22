from typing import Optional
from pydantic import BaseModel, Field, constr, AnyHttpUrl

from src.schemes.base.pyobject_id import PyObjectId


class Deal(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: constr(min_length=1)
    is_parent: bool # Determines whether a deal is parent.
    parent_id: Optional[PyObjectId] = None
    query_string: Optional[constr(min_length=1)] = None # Precalculated query string
    button_text: constr(min_length=1)
    image: AnyHttpUrl


class DealDetails(Deal):
    description: Optional[str] = None
