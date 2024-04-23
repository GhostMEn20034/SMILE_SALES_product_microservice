from typing import Optional, List
from pydantic import BaseModel, Field, conint, constr

from src.schemes.base.pyobject_id import PyObjectId


class CategoryShortInfo(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: constr(min_length=1)


class Category(CategoryShortInfo):
    level: conint(ge=0)
    parent_id: Optional[PyObjectId]
    tree_id: PyObjectId
    groups: Optional[List[constr(min_length=1)]]
