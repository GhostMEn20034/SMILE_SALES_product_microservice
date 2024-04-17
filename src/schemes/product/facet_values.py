from typing import Any, Optional, List, Union
from pydantic import BaseModel, constr, conint

class FacetValueItem(BaseModel):
    """
    Represents a single value item within a facet.
    This model captures the details of a facet value, including its unit, count, and display name.
    """
    # The actual value of the facet item.
    value: Any
    # The unit of measurement for the facet value, if applicable.
    unit: Optional[constr(min_length=1)] = None
    # The number of occurrences or frequency of the facet value.
    count: conint(ge=0)
    # The human-readable name for the facet value.
    display_name: constr(min_length=1)


class FacetValuesObject(BaseModel):
    """
    Encapsulates the values associated with a specific facet code and name.

    This model is used to store and transmit the collection of values that belong to a particular facet,
    along with an explanation for the facet.
    """
    # The unique code identifier for the facet.
    code: constr(min_length=1)
    # The human-readable name of the facet.
    name: constr(min_length=1)
    # Is Facet is Range Facet
    is_range: bool
    # A brief description or explanation of the facet.
    explanation: Optional[constr(min_length=1)]
    # A list of 'FacetValueItem' instances representing the facet's values.
    values: List[FacetValueItem]

