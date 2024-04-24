from typing import List, Dict
from bson import ObjectId, Decimal128

from src.param_classes.product.variation_options_retrieval_params import VariationOptionsRetrievalParams
from src.query_utils.product.facet_values_display_name import get_facets_display_name_switch_case
from src.query_utils.product.get_variations_query_helper import ProductVariationsQueryHelper
from src.aggregation_pipelines.product.product_list import get_discounted_price


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
            # Stage 1: remove all product's attributes where attribute.code is in option.field_codes
            {"$project": {
                "attrs": {
                    "$filter": {
                        "input": "$attrs",
                        "as": "attr",
                        "cond": {"$in": ["$$attr.code", option.field_codes]}
                    }
                },
            }},
            # Stage 2: Reformat product attributes to format:
            # {attribute.code: {attribute's value, unit, type key-value pairs}}
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
            # Stage 3: Group all attribute objects attribute.code,
            # and keys must be in the order as in option.field_codes
            {"$group": {
                "_id": variations_query_helper.get_group_keys()
            }},
            # Stage 4: Add display_name (user-friendly representation of attribute object) for each attribute object
            {"$addFields": variations_query_helper.get_display_name_for_each_attr_code()},
            # Stage 5: Add a joined_display_names (string representation of group of attributes) for each group of attributes.
            # This string is joined string from array of display names
            # from each attribute in the list (created from object of attributes)
            {"$project": {
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
            }},
            # Stage 6: remove "type" and "display_name" from each attribute object
            # and keep joined display_name that consists of each attribute's display_name.
            {"$project": variations_query_helper.get_projection_to_exclude_redundant_fields()},
            # Stage 7: Push all attributes to the "choices" array
            # and rename "$joined_display_names" to "display_name" for each attribute group
            {"$group": {
                "_id": None,
                "choices": {"$push": {"values": "$_id", "display_name": "$joined_display_names"}}
            }},
            # Stage 8: Sort all attributes by its unit of measurement and value
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


def get_pipeline_to_retrieve_product_details(product_id: ObjectId) -> List[Dict]:
    pipeline = [
        # Stage 1: Filter products by the specified product id.
        {"$match": {
            "_id": product_id,
        }},
        # Stage 2: Add user-friendly representation of attribute object
        # for each attribute and extra attribute
        {"$addFields": {
            "attrs": {
                '$map': {
                    'input': '$attrs',
                    'as': 'attr',
                    'in': {
                        "name": "$$attr.name",
                        "explanation": "$$attr.explanation",
                        "group": "$$attr.group",
                        "display_name": get_facets_display_name_switch_case(
                            "$attr.type",
                            "$attr.value",
                            "$attr.unit"
                        )
                    }
                }
            },
            "extra_attrs": {
                '$map': {
                    'input': '$extra_attrs',
                    'as': 'attr',
                    'in': {
                        "name": "$$attr.name",
                        "explanation": "$$attr.explanation",
                        "group": "$$attr.group",
                        "display_name": get_facets_display_name_switch_case(
                            "$attr.type",
                            "$attr.value",
                            "$attr.unit"
                        )
                    }
                }
            }
        }},
        # Stage 3: Group product's attributes by "group" field
        {"$addFields": {
            'attrs': {
                '$arrayToObject': {
                    '$map': {
                        'input': {
                            '$setUnion': [
                                '$attrs.group', [None]
                            ]
                        },
                        'as': 'group',
                        'in': {
                            'k': {
                                '$ifNull': ['$$group', "other"]
                            },
                            'v': {
                                '$filter': {
                                    'input': '$attrs',
                                    'as': 'attr',
                                    'cond': {
                                        '$eq': ['$$attr.group', '$$group']
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }},
        # Stage 4: Concat array with extra attributes and regular attributes without group
        # and add discounted price and discount percentage. Also, this stage calculates tax percentage.
        {"$addFields": {
            "discounted_price": get_discounted_price(),
            "discount_percentage": {
                "$cond": {
                    # if there's a discount rate
                    "if": {"$ne": ["$discount_rate", None]},
                    # Then, discount percentage is discount_rate * 100
                    "then": {"$multiply": ["$discount_rate", Decimal128("100.00")]},
                    # Otherwise, discount percentage is null
                    "else": None
                }
            },
            "original_price": "$price",
            "tax_percentage": {
                "$cond": {
                    # if there's a discount rate
                    "if": {"$ne": ["$tax_rate", None]},
                    # Then, discount percentage is discount_rate * 100
                    "then": {"$multiply": ["$tax_rate", Decimal128("100.00")]},
                    # Otherwise, discount percentage is null
                    "else": None
                }
            },
            "images": {
                '$concatArrays': [
                    ['$images.main'],
                    {'$ifNull': ['$images.secondaryImages', []]},
                ]
            },
            "attrs.other": {
                '$concatArrays': [
                    {'$ifNull': ['$attrs.other', []]},
                    {'$ifNull': ['$extra_attrs', []]}
                ]
            }
        }},
        # Stage 5: Exclude all unnecessary fields from projection
        {"$project": {
            "price": 0,
            "discount_rate": 0,
            "sku": 0,
            "external_id": 0,
            "parent": 0,
            "parent_id": 0,
            "same_images": 0,
            "variation_theme": 0,
            "is_filterable": 0,
            "category": 0,
            "search_terms": 0,
            "modified_at": 0,
            "extra_attrs": 0,
        }},
    ]

    return pipeline
