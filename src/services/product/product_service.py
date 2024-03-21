from typing import Dict, List

from bson import ObjectId
from fastapi import HTTPException

from src.repositories.product import ProductRepository
from src.schemes.product.filters import ProductFilters
from .filter_data_adapter import FilterDataAdapter
from .query_builders.query_filter_builder import ProductQueryFiltersBuilder
from .query_builders.search_query_builder import ProductSearchQueryBuilder
from src.repositories.category import CategoryRepository
from src.repositories.facet import FacetRepository
from src.param_classes.product.product_facet_params import ProductFacetParams


class ProductService:
    def __init__(self, product_repository: ProductRepository,
                 category_repository: CategoryRepository, facet_repository: FacetRepository):

        self.product_repository = product_repository
        self.category_repository = category_repository
        self.facet_repository = facet_repository

    # async def get_filtered_products(self, filters: ProductFilters):
    #     filter_data_adapter = FilterDataAdapter(filter_data=filters)
    #     filters_dto = filter_data_adapter.get_product_filters_dto()

    async def get_filtered_facet_values(self, filters: ProductFilters):
        # Convert all datatypes in product filters suitable for mongodb
        filter_data_adapter = FilterDataAdapter(filter_data=filters)
        filters_dto = filter_data_adapter.get_product_filters_dto()

        # Find category document by id, if category is specified and category not found, raise HTTP 404
        current_category = filters_dto.category
        # Whether category was automatically defined (True) or specified manually (False)
        auto_defined = False

        is_document_exist = await self.category_repository.is_document_exists({"_id": current_category})
        if not is_document_exist and current_category:
            raise HTTPException(status_code=404, detail="Specified category does not exist")

        query_filters_builder = ProductQueryFiltersBuilder(product_filters_dto=filters_dto)
        category_ids = []

        # if category id not specified in filters
        if not filters_dto.category:
            # Get filtered product count grouped by the category
            products_count: List[Dict] = await self.product_repository.get_product_count_by_category(
                query_filters_builder)
            # Get category_id from each dict in list, and if there are no categories, raise HTTP 404
            category_ids: List[ObjectId] = [product["category_id"] for product in products_count]
            if not category_ids:
                raise HTTPException(status_code=404, detail="No results were found with the given filters")

            auto_defined = True
            current_category = category_ids[0]
        else:
            category_ids.append(filters_dto.category)

        # get facets with ids from category_ids list
        facets: List[Dict] = await self.facet_repository.get_facet_codes_by_category_priority(category_ids)

        search_query_builder = ProductSearchQueryBuilder(query_filters_builder)
        product_facet_params = ProductFacetParams([facet["code"] for facet in facets], category_ids)
        # Get all possible filtered product' facet values
        facet_values_result = await self.product_repository.get_facet_values(search_query_builder, product_facet_params)
        # Get all category's ancestors and children
        category_relations = await self.category_repository.get_category_ancestors_and_children(current_category,
                                                                                                auto_defined)

        return {"facet_values": facet_values_result.facet_values,
                "price_range": facet_values_result.price_range_facet,
                "categories": category_relations, }
