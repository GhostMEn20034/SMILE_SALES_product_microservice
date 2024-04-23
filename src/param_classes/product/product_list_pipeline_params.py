from typing import Dict, List

from src.schemes.product.filters.product_list import ProductPaginationSettings


class ProductListPipelineParams:
    """
    Encapsulates parameters essential for creating product list aggregation pipeline
    """
    def __init__(self, filter_pipeline: List[Dict], pagination_settings: ProductPaginationSettings):
        # Pipeline stages like $search, $match etc.
        self.filter_pipeline = filter_pipeline
        # Class with page number, page size, sort option etc.
        self.pagination_settings = pagination_settings

