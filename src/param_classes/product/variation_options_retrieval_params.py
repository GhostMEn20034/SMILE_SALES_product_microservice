from bson import ObjectId

from src.schemes.variation_theme.base import VariationTheme


class VariationOptionsRetrievalParams:
    """
    Encapsulates parameters for retrieving options of product variations  .
    """
    def __init__(self, parent_id: ObjectId, variation_theme: VariationTheme):
        self.parent_id = parent_id # parent_id by which db will filter variations
        self.variation_theme: VariationTheme = variation_theme
