from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel

from .base import FacetValuesObject, PriceRangeFacet
from src.schemes.category.get import CategoryTree


class FacetValuesResponse(BaseModel):
    categories: CategoryTree
    price_range: Optional[PriceRangeFacet]
    facet_values: List[FacetValuesObject]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}
