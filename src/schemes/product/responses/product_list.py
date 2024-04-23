from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, conint, Field, constr, AnyHttpUrl

from src.schemes.base.pydecimal128 import PyDecimal128
from src.schemes.base.pyobject_id import PyObjectId

class ProductListItem(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: constr(min_length=1)
    discounted_price: PyDecimal128 = Field()
    original_price: PyDecimal128 = Field()
    discount_percentage: Optional[PyDecimal128] = Field(default=None)
    stock: conint(ge=0)
    max_order_qty: conint(ge=0)
    image: AnyHttpUrl


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

