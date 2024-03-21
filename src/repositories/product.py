from motor.motor_asyncio import AsyncIOMotorDatabase

from .base.base_repository import BaseRepository
from src.services.product.query_builders.search_query_builder import ProductSearchQueryBuilder
from src.aggregation_pipelines.product.product_count import get_pipeline_to_retrieve_product_count_by_category
from src.aggregation_pipelines.product.product_list import get_search_product_pipeline
from src.aggregation_pipelines.product.facet_values import get_pipeline_to_retrieve_price_range
from src.services.product.query_builders.query_filter_builder import ProductQueryFiltersBuilder
from src.param_classes.product.product_facet_params import ProductFacetParams
from src.result_classes.product.repository_results import FacetValueResults


class ProductRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, 'products')

    async def get_product_count_by_category(self, query_filters_builder: ProductQueryFiltersBuilder):
        """
        Return count of products by each category
        """
        # Add query filters to dict of filters
        filters = {}
        filters.update(query_filters_builder.build_price_range_filter())
        filters.update(query_filters_builder.build_category_filter())
        filters.update({"is_filterable": True, "for_sale": True, "parent": False})
        facet_filters = query_filters_builder.build_facet_filter()

        if facet_filters:
            filters.update({"$and": facet_filters})

        final_pipeline = []
        # Add search pipeline stage if search query in product filters dto is not None and has at least one character
        search_query = query_filters_builder.get_search_query()
        search_pipeline_stage = get_search_product_pipeline(search_query) if search_query else None
        if search_pipeline_stage:
            final_pipeline.extend(search_pipeline_stage)

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
        filters.update(search_query_builder.query_filters_builder.build_price_range_filter())
        filters.update(search_query_builder.query_filters_builder \
                       .build_multiple_category_filter(product_facet_params.category_ids))
        filters.update({
            "is_filterable": True, "for_sale": True, "parent": False
        })

        final_pipeline = []
        # Add search pipeline stage if search query in product filters dto is not None and has at least one character
        search_query = search_query_builder.query_filters_builder.get_search_query()
        search_pipeline_stage = get_search_product_pipeline(search_query,
                                                            exclude_low_relevant_results=True) if search_query else None
        if search_pipeline_stage:
            final_pipeline.extend(search_pipeline_stage)

        facet_pipelines = {}
        # Add price range facet
        facet_pipelines.update({'price_range': get_pipeline_to_retrieve_price_range()})
        # Get products' facet values for each facet code
        for facet_pipeline in search_query_builder.build_facet_pipelines(product_facet_params.facet_codes):
            facet_pipelines.update(facet_pipeline)

        # Add query filters to $match statement
        final_pipeline.append({"$match": filters})
        # Project only 'attrs' field to reduce document fields count to reduce load on the next pipeline stage
        final_pipeline.append({"$project": {"attrs": 1, "price": 1}})
        # Add each sub pipeline to $facet statement
        final_pipeline.append({"$facet": facet_pipelines})

        facet_values = await self.db[self.collection_name].aggregate(pipeline=final_pipeline).to_list(length=None)
        price_range_facet = {}

        if 'price_range' in facet_values[0]:
            price_range_facet = facet_values[0].pop('price_range')[0]

        result = []
        for key, value in facet_values[0].items():
            # If product's facet has values, then add it to final result
            if value:
                result.append(value[0])

        return FacetValueResults(facet_values=result, price_range_facet=price_range_facet)
