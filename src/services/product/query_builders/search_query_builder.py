from typing import List, Dict, Optional
from bson import ObjectId

from src.schemes.facet.base import Facet
from .query_filter_builder import ProductQueryFiltersBuilder
from src.services.product.sort_statement_builder import SortStatementBuilder
from src.aggregation_pipelines.product.facet_values import (
    get_pipeline_to_retrieve_regular_facet_values,
    get_pipeline_to_retrieve_range_facet_values,
    get_pipeline_to_retrieve_price_range
)
from src.aggregation_pipelines.product.product_list import (
    get_product_list_pipeline,
    get_search_product_pipeline,
    get_discounted_price,
)
from src.aggregation_pipelines.base.pagination_pipelines import get_pagination_to_skip_items
from src.param_classes.product.product_list_pipeline_params import ProductListPipelineParams


class ProductSearchQueryBuilder:
    """
    A builder class for constructing search query pipelines for products.

    This class uses a `ProductQueryFiltersBuilder` instance to create MongoDB
    aggregation pipelines that are tailored to retrieve facet values, product lists,
    and product details based on the current search query and selected facets.
    """

    def __init__(self, query_filters_builder: ProductQueryFiltersBuilder):
        self.query_filters_builder = query_filters_builder

    @staticmethod
    def get_discounted_price_field():
        return {"discounted_price": get_discounted_price()}

    def build_common_filters(self, category_ids: Optional[List[ObjectId]] = None,
                             add_facet_filters: bool = False) -> Dict:
        """
        Builds common filters for getting all facet values and product list.
        :param category_ids: List of categories to filter
        :param add_facet_filters: Whether to add facet filters to the $match filter stage
        """
        filters = {}
        filters.update(self.query_filters_builder.build_price_range_filter("discounted_price"))
        filters.update(self.query_filters_builder \
                       .build_multiple_category_filter(category_ids))
        filters.update({
            "for_sale": True, "parent": False,
        })
        if add_facet_filters:
            facet_filters = self.query_filters_builder.build_facet_filter()
            if facet_filters:
                filters.update({"$and": facet_filters})

        return filters

    def build_search_pipeline(self, query: Optional[str] = None) -> List[Dict]:
        """
        Builds search pipeline for product search.
        :param query: Query string for product string. Use it only if you need to specify other search query.
        If query don't specified it will get search query specified in query parameter class.
        """
        search_query = self.query_filters_builder.get_search_query() if query is None else query
        search_pipeline_stage = get_search_product_pipeline(search_query,
                                                            exclude_low_relevant_results=True) if search_query else None
        if search_pipeline_stage:
            return search_pipeline_stage

        return []

    def build_facet_pipelines(self, facets: List[Facet]):
        """
        Generates MongoDB aggregation pipelines for each facet code provided.
        These pipelines are designed to retrieve facet values while considering
        any previously chosen facets to refine the search results.
        """
        chosen_facet_keys = self.query_filters_builder.get_chosen_facets_keys()
        for facet in facets:
            current_facet_filter = None
            # if facet code in list of chosen facet keys
            if facet.code in chosen_facet_keys:
                facet_filter = []
                # Then add each chosen facet dictionary to the facet filters
                for index, chosen_facet in enumerate(self.query_filters_builder.build_facet_filter()):
                    # if current chosen facet code in nested iteration
                    # is not equal to current facet code in iteration above,
                    # then add facet filter to the list with the facet filters
                    if chosen_facet_keys.index(facet.code) != index:
                        facet_filter.append(chosen_facet)
                    else:
                        # Otherwise we will use this facet filter later (see on match_expression variable)
                        current_facet_filter = chosen_facet
            else:
                # if facet code not in list of chosen facet keys
                # then use all chosen facets for building facet filters
                facet_filter = self.query_filters_builder.build_facet_filter()

            # Facet's match expression.
            # To satisfy conditions, facet with the values must:
            match_expression = {"$or": [
                {"$and": facet_filter},  # 1) Either Matching facet filters
                current_facet_filter \
                if current_facet_filter else {"$expr": False} # 2) Or facet should be chosen by the user
            ]} if facet_filter else {} # If there's no facet filter, we don't apply any facet filter to the facet.

            if facet.is_range:
                yield get_pipeline_to_retrieve_range_facet_values(facet, match_expression)
            else:
                yield get_pipeline_to_retrieve_regular_facet_values(facet, match_expression)

    def build_price_range_facet(self):
        facet_filter = self.query_filters_builder.build_facet_filter()
        match_expression = {"$and": facet_filter} if facet_filter else {}

        return {'price_range': get_pipeline_to_retrieve_price_range(
            "discounted_price", match_expression)
        }

    def build_product_list_pipeline(self, product_list_pipeline_params: ProductListPipelineParams) -> List[Dict]:
        page = product_list_pipeline_params.pagination_settings.page
        page_size = product_list_pipeline_params.pagination_settings.page_size
        sort_option = product_list_pipeline_params.pagination_settings.sort_option

        sort_statement_builder = SortStatementBuilder(sort_option)

        pipeline = [
            *product_list_pipeline_params.filter_pipeline,
            {"$facet": {
                "items": [
                    *get_product_list_pipeline(),
                    *sort_statement_builder.get_sort_pipeline_stage(),
                    *get_pagination_to_skip_items(page, page_size)
                ],
                "count": [
                    {
                        "$count": "count",
                    }
                ],
            }},
            {"$unwind": "$count"},
            {"$project": {
                "items": 1,
                "count": "$count.count",
            }}
        ]

        return pipeline
