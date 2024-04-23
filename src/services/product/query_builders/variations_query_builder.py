from src.param_classes.product.variation_options_retrieval_params import VariationOptionsRetrievalParams
from src.aggregation_pipelines.product.product_details import get_pipeline_for_variation_options_retrieval
from src.aggregation_pipelines.product.product_list import get_variations_list_pipeline


class VariationsQueryBuilder:
    """
    Class to build queries for operations on product variations.
    """
    @staticmethod
    def get_query_to_retrieve_variation_options(variation_options_retrieval_params: VariationOptionsRetrievalParams):
        variation_options_pipeline = get_pipeline_for_variation_options_retrieval(variation_options_retrieval_params)
        return variation_options_pipeline

    @staticmethod
    def get_query_to_retrieve_product_variations(variation_options_retrieval_params: VariationOptionsRetrievalParams):
        attribute_codes = []
        for option in variation_options_retrieval_params.variation_theme.options:
            attribute_codes.extend(option.field_codes)

        return get_variations_list_pipeline(variation_options_retrieval_params.parent_id, attribute_codes)


