from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, constr, AnyHttpUrl, conint

from src.schemes.base.pyobject_id import PyObjectId


class EventStatusEnum(str, Enum):
    created = "created"
    started = "started"
    ended = "ended"


class EventItem(BaseModel):
    """
    Model representing an event item in list or in similar structures
    """
    id: PyObjectId = Field(alias='_id')
    name: constr(min_length=1)
    start_date: datetime
    end_date: datetime
    status: EventStatusEnum
    image: AnyHttpUrl


class EventDetails(EventItem):
    """
    Detail representation of an event
    """
    description: Optional[str]


class ProductCountByCategoryItem(BaseModel):
    """
    Represents the item which contains count of products per category
    """
    id: PyObjectId = Field(alias='_id')
    name: constr(min_length=1)
    count: conint(ge=0)


