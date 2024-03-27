from typing import List, Optional, Any
from bson import ObjectId
from pydantic import BaseModel, conint

from .base import FacetValuesObject, PriceRangeFacet, ProductListItem
from src.schemes.category.get import CategoryTree


class FacetValuesResponse(BaseModel):
    categories: CategoryTree
    price_range: Optional[PriceRangeFacet]
    facet_values: List[FacetValuesObject]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}


class ProductListResponse(BaseModel):
    items: List[ProductListItem] = []
    count: conint(ge=0) = 0

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}

