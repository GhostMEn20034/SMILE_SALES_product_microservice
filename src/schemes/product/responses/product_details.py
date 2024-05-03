from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, constr, conint, AnyHttpUrl

from src.schemes.base.pydecimal128 import PyDecimal128
from src.schemes.base.pyobject_id import PyObjectId
from src.schemes.category.base import CategoryShortInfo


class ProductDetailsAttribute(BaseModel):
    """
    Short representation of product's attribute
    """
    name: constr(min_length=1)
    explanation: Optional[constr(min_length=1)] = None
    display_name: constr(min_length=1)


class ProductDetailsItem(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: constr(min_length=1)
    discounted_price: PyDecimal128 = Field()
    original_price: PyDecimal128 = Field()
    discount_percentage: Optional[PyDecimal128] = Field(default=None)
    stock: conint(ge=0)
    max_order_qty: conint(ge=0)
    images: List[AnyHttpUrl]
    for_sale: bool
    attrs: Dict[str, List[ProductDetailsAttribute]]
    created_at: datetime


class ProductDetailsResponse(BaseModel):
    item: ProductDetailsItem
    category_hierarchy: List[CategoryShortInfo]

