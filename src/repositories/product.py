from math import ceil
from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .base.base_repository import BaseRepository
from src.services.product.query_builders.search_query_builder import ProductSearchQueryBuilder
from src.aggregation_pipelines.product.product_count import get_pipeline_to_retrieve_product_count_by_category
from src.param_classes.product.product_facet_params import ProductFacetParams
from src.param_classes.product.product_list_pipeline_params import ProductListPipelineParams
from src.schemes.product.filters import ProductPaginationSettings
from src.result_classes.product.repository_results import FacetValueResults


class ProductRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, 'products')

    async def get_product_count_by_category(self, search_query_builder: ProductSearchQueryBuilder):
        """
        Return count of products by each category
        """
        # Add query filters to dict of filters
        filters = {}
        filters.update(search_query_builder.build_common_filters(add_facet_filters=True))

        final_pipeline = []
        # Add search pipeline stage if search query in product filters dto is not None and has at least one character
        final_pipeline.extend(search_query_builder.build_search_pipeline())
        # Add discounted price field to the result
        final_pipeline.append({"$addFields": ProductSearchQueryBuilder.get_discounted_price_field()})
        # Add filters to pipeline
        final_pipeline.append({"$match": filters})
        # Extend main pipeline by pipeline to get product count by category
        final_pipeline.extend(get_pipeline_to_retrieve_product_count_by_category())
        products_count = await self.db[self.collection_name].aggregate(pipeline=final_pipeline).to_list(length=None)
        return products_count

    async def get_facet_values(self, search_query_builder: ProductSearchQueryBuilder,
                               product_facet_params: ProductFacetParams):
        # Add query filters to dict of filters
        filters = {}
        filters.update(search_query_builder.build_common_filters(product_facet_params.category_ids))
        filters.update({
            "is_filterable": True
        })
        final_pipeline = []
        # Add search pipeline stage if search query in product filters dto is not None and has at least one character
        final_pipeline.extend(search_query_builder.build_search_pipeline())
        # Add discounted price field to the result
        final_pipeline.append({"$addFields": search_query_builder.get_discounted_price_field()})
        # Add query filters to $match statement
        final_pipeline.append({"$match": filters})

        facet_pipelines = {}
        # Add price range facet
        facet_pipelines.update(search_query_builder.build_price_range_facet())
        # Get products' facet values for each facet code
        for facet_pipeline in search_query_builder.build_facet_pipelines(product_facet_params.facet_codes):
            facet_pipelines.update(facet_pipeline)

        # Project only 'attrs' field to reduce document fields count to reduce load on the next pipeline stage
        final_pipeline.append({"$project": {"attrs": 1, "discounted_price": 1}})
        # Add each sub pipeline to $facet statement
        final_pipeline.append({"$facet": facet_pipelines})

        facet_values = await self.db[self.collection_name].aggregate(pipeline=final_pipeline).to_list(length=None)
        price_range_facet = None

        if 'price_range' in facet_values[0] and facet_values[0].get('price_range'):
            price_range_facet = facet_values[0].pop('price_range')[0]

        result = []
        for key, value in facet_values[0].items():
            # If product's facet has values, then add it to final result
            if value:
                result.append(value[0])

        return FacetValueResults(facet_values=result, price_range_facet=price_range_facet)

    async def get_filtered_products(self, search_query_builder: ProductSearchQueryBuilder,
                                    pagination_settings: ProductPaginationSettings,
                                    category_ids: List[ObjectId]):
        # Add query filters to dict of filters
        filters = {}
        filters.update(search_query_builder.build_common_filters(category_ids, add_facet_filters=True))

        filter_pipeline = []
        # Add search pipeline stage if search query in product filters dto is not None and has at least one character
        filter_pipeline.extend(search_query_builder.build_search_pipeline())
        # Add discounted price field to the result
        filter_pipeline.append({"$addFields": search_query_builder.get_discounted_price_field()})
        # Add query filters to $match statement
        filter_pipeline.append({"$match": filters})

        product_list_pipeline_params = ProductListPipelineParams(filter_pipeline, pagination_settings)
        # Retrieve the final pipeline and execute it.
        final_pipeline = search_query_builder.build_product_list_pipeline(product_list_pipeline_params)
        products_data = await self.db[self.collection_name].aggregate(final_pipeline).to_list(length=None)
        if not products_data:
            return {}

        result = {
            "items": products_data[0].get("items"),
            "count": products_data[0].get("count"),
        }
        result["page_count"] = ceil(result["count"] / pagination_settings.page_size)
        return result
