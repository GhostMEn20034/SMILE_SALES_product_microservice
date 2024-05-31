from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, conint

from .base import EventItem, EventDetails, ProductCountByCategoryItem


class EventListResponse(BaseModel):
    items: List[EventItem]
    count: conint(ge=0) = 0
    page_count: conint(ge=0) = 1

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}


class EventDetailsResponse(BaseModel):
    item: EventDetails
    product_count_by_category: Optional[List[ProductCountByCategoryItem]]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}
