from typing import List, Optional, Dict
from bson import ObjectId
from pydantic import BaseModel, conint

from .base import ProductListItem
from .price_range import PriceRangeFacet
from .facet_values import FacetValuesObject
from src.schemes.category.get import CategoryTree
from src.schemes.facet.facet_metadata import FacetMetadataItem


class FacetValuesResponse(BaseModel):
    """
    Represents the response with List of facet values, price range, category tree and facet metadata
    """
    categories: CategoryTree
    price_range: Optional[PriceRangeFacet]
    facet_values: List[FacetValuesObject]
    facet_metadata: Dict[str, FacetMetadataItem]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}


class ProductListResponse(BaseModel):
    """
    Represents the response with list of products
    """
    items: List[ProductListItem] = []
    count: conint(ge=0) = 0
    page_count: conint(ge=0) = 1

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}

