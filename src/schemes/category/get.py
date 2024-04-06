from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field

from src.schemes.base.pyobject_id import PyObjectId


class CategoryTreeElement(BaseModel):
    """
    Represents a single element within a category tree.
    This base model defines the structure of a category element with an identifier and a name.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str


class CurrentTreeElement(CategoryTreeElement):
    """
    Extends the CategoryTreeElement with a flag indicating auto-definition.

    This model is used to represent the current category element in the tree,
    with an additional attribute to indicate if it was auto-defined.
    """
    # A flag to indicate whether the category element was auto-defined.
    auto_defined: bool = False


class CategoryTree(BaseModel):
    """
    Represents the hierarchical structure of a category within a catalog.

    This model holds the current category, along with its ancestors and children,
    providing a complete view of its placement within the category tree.

    Attributes:
        current (CurrentTreeElement): The current category element, which may be auto-defined.
        nearest_children (List[CategoryTreeElement]): A list of category elements that are direct descendants of the current category.
        ancestors (List[CategoryTreeElement]): A list of category elements that are direct ancestors of the current category.
    """
    current: CurrentTreeElement
    nearest_children: List[CategoryTreeElement]
    ancestors: List[CategoryTreeElement]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}
