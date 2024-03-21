from typing import List, Optional, Dict
from bson import ObjectId

from src.schemes.product.dto.filters import ProductFiltersDto


class ProductQueryFiltersBuilder:
    """
    A builder class for creating query filters based on product filter criteria.

    This class takes a `ProductFiltersDto` object as input and provides methods to
    construct various query filters for a product search. These filters include
    facet filters, price range filters, and category filters.
    """
    def __init__(self, product_filters_dto: ProductFiltersDto):
        self.product_filters_dto = product_filters_dto

    def get_chosen_facets_keys(self) -> List[str]:
        return list(self.product_filters_dto.chosen_facets.keys())

    def get_search_query(self):
        return self.product_filters_dto.q

    def build_facet_filter(self) -> List[Dict]:
        """
        Builds filter based on chosen facets
        """
        if self.product_filters_dto.chosen_facets is None:
            return []

        facet_filters = []

        for facet_code in self.product_filters_dto.chosen_facets:
            if len(self.product_filters_dto.chosen_facets[facet_code]) > 0:
                facet_filters.append(
                    {"attrs": {"$elemMatch": {"$or": self.product_filters_dto.chosen_facets[facet_code]}}}
                )

        return facet_filters

    def build_price_range_filter(self) -> Dict:
        """
        Builds filter to select documents with price in range from min_price to max_price
        """
        price_range_filter = {}
        if self.product_filters_dto.min_price:
            price_range_filter["$gte"] = self.product_filters_dto.min_price

        if self.product_filters_dto.max_price:
            price_range_filter["$lte"] = self.product_filters_dto.max_price

        if not price_range_filter:
            return {}

        return {"price": price_range_filter}

    def build_category_filter(self):
        """
        Builds filter to select documents where category equals to category ProductFiltersDto
        """
        category_filter = {}
        if self.product_filters_dto.category:
            category_filter["category"] = self.product_filters_dto.category

        return category_filter

    @staticmethod
    def build_multiple_category_filter(categories: Optional[List[ObjectId]] = None):
        """
        Builds filter to select documents where category in specified categories list
        """
        category_filter = {}
        if categories:
            category_filter["$in"] = categories

        if not category_filter:
            return {}

        return {"category": category_filter}
