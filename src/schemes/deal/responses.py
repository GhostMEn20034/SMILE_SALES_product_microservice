from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, conint

from .base import Deal, DealDetails


class DealListResponse(BaseModel):
    items: List[Deal] = []
    count: conint(ge=0) = 0
    page_count: conint(gt=0) = 1

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}


class DealDetailsResponse(BaseModel):
    item: DealDetails
    children: List[Deal] = []

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}