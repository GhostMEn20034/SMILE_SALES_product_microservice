import json
from bson.decimal128 import Decimal128

from src.schemes.product.filters import ProductFilters
from src.schemes.product.dto.filters import ProductFiltersDto


class FilterDataAdapter:
    """
    Adapts product filters, so MongoDB can use these filters for queries
    """
    def __init__(self, filter_data: ProductFilters):
        self.filter_data = filter_data

    def _get_chosen_facets_from_bytes(self) -> dict:
        """
        Decodes bytes to dict
        """
        if self.filter_data.chosen_facets is not None:
            chosen_facets = json.loads(self.filter_data.chosen_facets)
            return chosen_facets

        return {}

    def get_product_filters_dto(self) -> ProductFiltersDto:
        # Get minimum price and convert it to Decimal128 if value exists
        min_price = Decimal128(self.filter_data.min_price) if self.filter_data.min_price is not None else None
        # Get maximum price and convert it to Decimal128 if value exists
        max_price = Decimal128(self.filter_data.max_price) if self.filter_data.max_price is not None else None
        # Get facets as dict
        chosen_facets = self._get_chosen_facets_from_bytes()

        return ProductFiltersDto(
            min_price=min_price,
            max_price=max_price,
            category=self.filter_data.category,
            q=self.filter_data.q,
            chosen_facets=chosen_facets,
        )
