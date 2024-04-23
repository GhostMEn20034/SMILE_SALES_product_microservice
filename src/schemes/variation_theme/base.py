from typing import List
from pydantic import BaseModel, constr, Field

from src.schemes.base.pyobject_id import PyObjectId


class VariationThemeOption(BaseModel):
    name: constr(min_length=1) # Option's name
    field_codes: List[constr(min_length=1)] # List of attribute fields


class VariationTheme(BaseModel):
    """
    VariationTheme is conception that determines what fields are different in related product variations
    """
    name: constr(min_length=1) # Variation theme's name
    options: List[VariationThemeOption]
