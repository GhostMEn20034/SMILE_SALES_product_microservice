from typing import List

from .query_filter_builder import ProductQueryFiltersBuilder
from src.aggregation_pipelines.product.facet_values import get_pipeline_to_retrieve_facet_values


class ProductSearchQueryBuilder:
    """
    A builder class for constructing search query pipelines for products.

    This class uses a `ProductQueryFiltersBuilder` instance to create MongoDB
    aggregation pipelines that are tailored to retrieve facet values, product lists,
    and product details based on the current search query and selected facets.
    """

    def __init__(self, query_filters_builder: ProductQueryFiltersBuilder):
        self.query_filters_builder = query_filters_builder

    def build_facet_pipelines(self, facet_codes: List[str]):
        """
        Generates MongoDB aggregation pipelines for each facet code provided.
        These pipelines are designed to retrieve facet values while considering
        any previously chosen facets to refine the search results.
        """
        chosen_facet_keys = self.query_filters_builder.get_chosen_facets_keys()
        for code in facet_codes:
            if code in chosen_facet_keys:
                facet_filter = self.query_filters_builder.build_facet_filter()[0: chosen_facet_keys.index(code)]
            else:
                facet_filter = self.query_filters_builder.build_facet_filter()

            match_statement = {"$and": facet_filter} if facet_filter else {}

            yield get_pipeline_to_retrieve_facet_values(code, match_statement)

    def build_product_list_pipeline(self):
        pass
