from typing import Optional
from pydantic import BaseModel, constr, conint, Field, AnyHttpUrl

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
