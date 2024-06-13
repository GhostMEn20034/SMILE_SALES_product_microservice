from typing import Optional

from src.schemes.base.pyobject_id import PyObjectId


class CategoryListParams:
    def __init__(self, parent_id: Optional[PyObjectId] = None):
        self.parent_id = parent_id
