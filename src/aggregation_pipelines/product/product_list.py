from typing import Dict, List

from bson import ObjectId
from bson.decimal128 import Decimal128

from src.config.settings import settings
from src.query_utils.common.search_relevance import get_pipeline_to_exclude_low_relevant_search_items
from src.query_utils.product.get_variations_query_helper import ProductVariationsQueryHelper


def get_search_product_pipeline(query: str, exclude_low_relevant_results: bool = False) -> List[Dict]:
    if not query.strip():
        return []

    search_product_pipeline = [
        {'$search': {
            'index': settings.atlas_search_product_index_name.strip(),
            'compound': {
                'should': [
                    {
                        'text': {
                            'query': query.strip(),
                            'path': {"wildcard": "*"},  # Searches all fields for the text query.
                        }
                    },
                    {
                        'compound': {
                            'should': [
                                # A phrase query searches for the exact phrase with some leniency.
                                {"phrase": {
                                    "query": query.strip(),
                                    "path": "name",
                                    "slop": 20,  # Allows for some word rearrangement in the phrase.
                                    "score": {"boost": {"value": 2.4}},  # Boosts the relevance score if matched.
                                }},
                                {"phrase": {
                                    "query": query.strip(),
                                    "path": "search_terms",
                                    "slop": 12,  # Allows for some word rearrangement in the phrase.
                                    "score": {"boost": {"value": 1.3}},  # Boosts the relevance score if matched.
                                }},
                            ]
                        }
                    }
                ],
            }
        }
        }
    ]

    if exclude_low_relevant_results:
        search_product_pipeline.extend(get_pipeline_to_exclude_low_relevant_search_items(settings.relevance_threshold))

    return search_product_pipeline


def get_product_list_pipeline() -> List[Dict]:
    pipeline = [
        {"$project": {
            "name": 1,
            # The price including the discount
            "discounted_price": 1,
            "original_price": "$price",
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
            "stock": 1,
            "max_order_qty": 1,
            # Product's main image
            "image": "$images.main"
        }}
    ]

    return pipeline


def get_discounted_price():
    return {
            "$cond": {
                # if product has discount rate
                "if": {"$ne": ["$discount_rate", None]},
                # Then, new price will: original price - (original_price * discount rate)
                "then": {"$round": [{"$subtract":
                                         ["$price",
                                          {"$multiply": ["$price", "$discount_rate"]}
                                          ]
                                     }, 2]},
                # Otherwise, new price is original price
                "else": "$price"
            }
    }


def get_variations_list_pipeline(parent_id: ObjectId, attribute_codes: List[str]) -> List[Dict]:

    variations_query_helper = ProductVariationsQueryHelper(attribute_codes,
                                                           "variation_attributes")

    pipeline = [
        {"$match": {
            "parent": False,
            "parent_id": parent_id,
        }},
        {"$project": {
           "name": 1,
           "variation_attributes": {
               "$filter": {
                   "input": "$attrs",
                   "as": "attr",
                   "cond": {"$in": ["$$attr.code", attribute_codes]}
               }
           }
        }},
        {"$project": {
           "name": 1,
           "variation_attributes": {
               "$arrayToObject": {
                   "$map": {
                       "input": "$variation_attributes",
                       "as": "attr",
                       "in": {
                           "k": "$$attr.code",
                           "v": {
                               "value": "$$attr.value",
                               "unit": "$$attr.unit",
                           }
                       }
                   }
               }
           }
        }},
        {"$sort": variations_query_helper.get_sort_keys_for_attributes()},
    ]

    return pipeline
