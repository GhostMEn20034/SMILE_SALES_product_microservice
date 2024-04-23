from typing import Optional, List, Dict
from bson import ObjectId
from pydantic import BaseModel

from src.schemes.category.get import CategoryTree
from src.schemes.facet.facet_metadata import FacetMetadataItem
from src.schemes.product.facet_values.facet_values_object import FacetValuesObject
from src.schemes.product.facet_values.price_range import PriceRangeFacet


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
