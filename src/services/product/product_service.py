from typing import Dict, List
from bson import ObjectId
from fastapi import HTTPException

from src.services.product.product_data_adapter import FilterDataAdapter
from .query_builders.query_filter_builder import ProductQueryFiltersBuilder
from .query_builders.search_query_builder import ProductSearchQueryBuilder
from src.schemes.product.filters import ProductFilters, ProductPaginationSettings
from src.schemes.product.get import ProductListResponse, FacetValuesResponse
from src.repositories.product import ProductRepository
from src.repositories.category import CategoryRepository
from src.repositories.facet import FacetRepository
from src.param_classes.product.product_facet_params import ProductFacetParams
from src.services.search_term.search_term_service import SearchTermService


class ProductService:
    def __init__(self, product_repository: ProductRepository, category_repository: CategoryRepository,
                 facet_repository: FacetRepository, search_term_service: SearchTermService):

        self.product_repository = product_repository
        self.category_repository = category_repository
        self.facet_repository = facet_repository
        self.search_term_service = search_term_service

    async def get_filtered_facet_values(self, filters: ProductFilters) -> FacetValuesResponse:
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
        search_query_builder = ProductSearchQueryBuilder(query_filters_builder)
        facets_category_ids = []

        # if category id not specified in filters
        if not filters_dto.category:
            # Get filtered product count grouped by the category
            products_count: List[Dict] = await self.product_repository.get_product_count_by_category(
                search_query_builder)
            # Get category_id from each dict in list, and if there are no categories, raise HTTP 404
            facets_category_ids: List[ObjectId] = [product["category_id"] for product in products_count]
            if not facets_category_ids:
                raise HTTPException(status_code=404, detail="No results were found with the given filters")

            auto_defined = True
            current_category = facets_category_ids[0]
        else:
            facets_category_ids.append(filters_dto.category)

        # Get all category's ancestors and children
        category_relations = await self.category_repository.get_category_ancestors_and_children(current_category,
                                                                                                auto_defined)
        products_category_ids = facets_category_ids.copy()
        if children := category_relations.get("all_children", []):
            products_category_ids.extend([category["_id"] for category in children])

        # get facets with ids from category_ids list
        facets: List[Dict] = await self.facet_repository.get_facet_codes_by_category_priority(facets_category_ids)
        product_facet_params = ProductFacetParams([facet["code"] for facet in facets], products_category_ids)
        # Get all possible filtered product' facet values
        facet_values_result = await self.product_repository.get_facet_values(search_query_builder, product_facet_params)

        return FacetValuesResponse(facet_values=facet_values_result.facet_values,
                                   price_range=facet_values_result.price_range_facet,
                                   categories=category_relations)

    async def get_product_list(self, filters: ProductFilters,
                               pagination_settings: ProductPaginationSettings) -> ProductListResponse:
        # Convert all datatypes in product filters suitable for mongodb
        filter_data_adapter = FilterDataAdapter(filter_data=filters)
        filters_dto = filter_data_adapter.get_product_filters_dto()

        query_filters_builder = ProductQueryFiltersBuilder(product_filters_dto=filters_dto)
        search_query_builder = ProductSearchQueryBuilder(query_filters_builder)

        if filters_dto.q:
            await self.search_term_service.increment_searched_count(filters_dto.q)

        if filters_dto.category:
            # If user specified the category, then get all child categories by which products will be filtered
            category_children = await self.category_repository \
                .get_category_children(filters_dto.category)
            category_ids = [filters_dto.category, ]
            category_ids.extend([category["_id"] for category in category_children])
        else:
            # If user did not specify the category, then no need to filter products by categories
            category_ids = []

        products_data = await self.product_repository \
            .get_filtered_products(search_query_builder, pagination_settings, category_ids)

        return ProductListResponse(**products_data)
