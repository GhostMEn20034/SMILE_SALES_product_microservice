from typing import Optional
from pydantic import BaseModel, conint

from src.schemes.base.pyobject_id import PyObjectId


class CategoryListFilters(BaseModel):
    parent_id: Optional[PyObjectId] = None
    level: Optional[conint(ge=0)] = None
