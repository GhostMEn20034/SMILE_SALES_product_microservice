from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel

from .base import CategoryShortInfo

class CategoryItem(CategoryShortInfo):
    nearest_children: List[CategoryShortInfo]

class CategoryListResponse(BaseModel):
    items: List[CategoryItem]
    parent_data: Optional[CategoryShortInfo]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}
