from typing import Dict, List
from bson import ObjectId
from fastapi import HTTPException

from .product_data_adapter import FilterDataAdapter
from .query_builders.query_filter_builder import ProductQueryFiltersBuilder
from .query_builders.search_query_builder import ProductSearchQueryBuilder
from src.schemes.product.filters.product_list import ProductFilters, ProductPaginationSettings
from src.schemes.product.responses.get_variations import GetVariationsResponse
from src.schemes.product.responses.facet_values import FacetValuesResponse
from src.schemes.product.responses.product_list import ProductListResponse
from src.schemes.product.responses.product_details import ProductDetailsResponse
from src.schemes.facet.base import Facet
from src.schemes.category.base import CategoryShortInfo
from src.schemes.variation_theme.base import VariationTheme
from src.repositories.product import ProductRepository
from src.repositories.category import CategoryRepository
from src.repositories.facet import FacetRepository
from src.param_classes.product.product_facet_params import ProductFacetParams
from src.param_classes.product.variation_options_retrieval_params import VariationOptionsRetrievalParams
from src.services.search_term.search_term_service import SearchTermService
from src.utils.facet.facet_metadata_provider import FacetMetadataProvider


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
        facet_objects = [Facet(**facet) for facet in facets]
        product_facet_params = ProductFacetParams(facet_objects, products_category_ids)
        # Get all possible filtered product' facet values
        facet_values_result = await self.product_repository.get_facet_values(search_query_builder, product_facet_params)
        facet_metadata_provider = FacetMetadataProvider(facet_objects)
        return FacetValuesResponse(
            facet_values=facet_values_result.facet_values,
            price_range=facet_values_result.price_range_facet,
            categories=category_relations,
            facet_metadata=facet_metadata_provider.get_facet_metadata(),
        )

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

    async def get_product_variations_and_options(self, product_id: ObjectId) -> GetVariationsResponse:
        product = await self.product_repository.get_one_document({"_id": product_id},
                                                                 {"variation_theme": 1, "parent": 1,
                                                                  "parent_id": 1})

        if not product:
            raise HTTPException(status_code=404, detail="Specified product does not exist")

        variation_theme = product["variation_theme"]
        if variation_theme is None:
            raise HTTPException(status_code=400, detail="Given product doesn't have variation theme")

        parent_id = product["parent_id"] if not product["parent"] else product_id

        variation_theme_object = VariationTheme(**variation_theme)
        variation_options_retrieval_params = VariationOptionsRetrievalParams(parent_id,
                                                                             variation_theme_object)
        variation_options = await self.product_repository.get_variation_options(
            variation_options_retrieval_params
        )

        variations = await self.product_repository.get_product_variations(variation_options_retrieval_params)
        variation_summary = {
            "variation_count": len(variations),
            "variation_options": variation_options,
        }

        return GetVariationsResponse(
            items=variations,
            variation_summary=variation_summary,
        )

    async def get_product_by_id(self, product_id: ObjectId) -> ProductDetailsResponse:
        product = await self.product_repository.get_one_document({"_id": product_id},
                                                                 {"parent": 1, "category": 1})
        if not product:
            raise HTTPException(status_code=404, detail="Product with the specified ID does not exist")

        if product["parent"]:
            raise HTTPException(status_code=400, detail="Parent product cannot be sold")

        product_details = await self.product_repository.get_product_details(product_id)
        category_relations = await self.category_repository.get_category_ancestors_and_children(product["category"])
        category_list = [
            CategoryShortInfo(**category_object) for category_object in category_relations.get("ancestors", [])
        ]
        category_list.append(CategoryShortInfo(**category_relations.get("current", {})))


        return ProductDetailsResponse(item=product_details,
                                      category_hierarchy=category_list,)
