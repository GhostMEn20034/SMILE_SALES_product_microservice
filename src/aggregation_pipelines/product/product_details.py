from typing import List, Dict

from src.param_classes.product.variation_options_retrieval_params import VariationOptionsRetrievalParams
from src.query_utils.product.get_variations_query_helper import ProductVariationsQueryHelper


def get_pipeline_for_variation_options_retrieval(
        variation_options_retrieval_params: VariationOptionsRetrievalParams) -> List[Dict]:
    """
    Returns an aggregation pipeline for retrieval options of product variations.
    """
    attribute_codes = []
    for option in variation_options_retrieval_params.variation_theme.options:
        attribute_codes.extend(option.field_codes)



    facet_pipeline_stage = {}
    for option in variation_options_retrieval_params.variation_theme.options:
        variations_query_helper = ProductVariationsQueryHelper(option.field_codes)
        facet_pipeline_stage["-".join(option.field_codes)] = [
            {"$project": {
                "attrs": {
                    "$filter": {
                        "input": "$attrs",
                        "as": "attr",
                        "cond": {"$in": ["$$attr.code", option.field_codes]}
                    }
                },
            }},
            {"$project": {
                "_id": 1,
                "values": {
                    "$arrayToObject": {
                        "$map": {
                            "input": "$attrs",
                            "as": "attr",
                            "in": {
                                "k": "$$attr.code",
                                "v": {
                                    "value": "$$attr.value",
                                    "unit": "$$attr.unit",
                                    "type": "$$attr.type",
                                }
                            }
                        }
                    }
                }
            }},
            {"$group": {
                "_id": variations_query_helper.get_group_keys()
            }},
            {"$addFields": variations_query_helper.get_display_name_for_each_attr_code()},
            {
                "$project": {
                    "joined_display_names": {
                        "$reduce": {
                            "input": {"$objectToArray": "$_id"},
                            "initialValue": "",
                            'in': {
                                '$concat': [
                                    '$$value',
                                    {'$cond': [{'$eq': ['$$value', '']}, '', ' | ']},
                                    '$$this.v.display_name'
                                ]
                            }
                        }
                    }
                }
            },
            {"$project": variations_query_helper.get_projection_to_exclude_redundant_fields()},
            {"$group": {
                "_id": None,
                "choices": {"$push": {"values": "$_id", "display_name": "$joined_display_names"}}
            }},
            {"$project": {
                "_id": 0,
                "option_name": option.name,
                "attribute_codes": option.field_codes,
                "choices": {
                    "$sortArray": {
                        "input": "$choices",
                        "sortBy": variations_query_helper.get_sort_keys_for_attributes(attr_group_key_name="values")
                    }
                }
            }},
        ]

    pipeline = [
        {"$match": {
            "parent_id": variation_options_retrieval_params.parent_id
        }},
        {"$project": {
            "attrs": {
                "code": 1,
                "value": 1,
                "unit": 1,
                "type": 1,
            },
        }},
        {"$project": {
            "attrs": {
                "$filter": {
                    "input": "$attrs",
                    "as": "attr",
                    "cond": {"$in": ["$$attr.code", attribute_codes]}
                }
            },
        }},
        {"$facet": facet_pipeline_stage}
    ]

    return pipeline
