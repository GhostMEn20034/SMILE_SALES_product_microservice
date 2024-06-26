from typing import Optional, Dict, List

from src.query_utils.product.boundary_handler import BoundaryHandler
from src.schemes.facet.base import Facet
from src.config.constants import MAX_SAFE_INTEGER


def get_pipeline_to_retrieve_regular_facet_values(facet: Facet, match_statement: dict) -> Dict:
    """
    Returns the pipeline to retrieve the regular facet's values
    :param facet: The facet object.
    :param match_statement: The pipeline stage to filtering products from which values are given
    """
    return {
        facet.code: [
            {"$match": match_statement},
            {"$unwind": "$attrs"},
            {"$unwind": "$attrs.value"},
            {"$match": {"attrs.code": facet.code}},
            {"$group": {"_id": {"code": "$attrs.code", "value": "$attrs.value", "unit": "$attrs.unit"},
                        "count": {"$sum": 1}}
             },
            {"$sort": {"_id.value": 1, "_id.unit": 1, "_id.code": 1}},
            {"$group": {"_id": "$_id.code",
                        "values": {"$push": {
                            "value": "$_id.value",
                            "unit": "$_id.unit",
                            "count": "$count",
                        }},
            }},
            {"$project": {
                "_id": 0,
                "code": "$_id",
                "name": facet.name,
                "type": facet.type,
                "is_range": {"$toBool": False},
                "values": 1,
            }},
        ]
    }


def get_pipeline_to_retrieve_range_facet_values(facet: Facet, match_statement: dict):
    """
    Returns the pipeline to retrieve the range facet's values (Ranges like: from 16 to 32 GB)
    :param facet: The facet object.
    :param match_statement: The pipeline stage to filtering products from which values are given
    """
    range_values = facet.range_values

    gte_field_to_range_mapping = {
        item.gteq: {"gteq": item.gteq, "ltn": item.ltn}
        for item in range_values
    }

    boundary_items = [item.gteq for item in range_values]
    boundary_handler = BoundaryHandler()

    return {
        facet.code: [
            {"$match": match_statement},
            {"$unwind": "$attrs"},
            {"$match": {"attrs.code": facet.code}},
            {
                "$bucket": {
                    "groupBy": "$attrs.value",
                    "boundaries": [*boundary_items, MAX_SAFE_INTEGER],
                    "default": "Other",
                    "output": {
                        "count": {"$sum": 1}
                    }
                }
            },
            {"$addFields": {
                "value": boundary_handler.get_boundary_value(gte_field_to_range_mapping),
            }},
            {"$group": {
                    "_id": None,
                    "values": {
                        "$push": {
                            "count": "$count",
                            "value": "$value",
                        }
                    },
            }},
            {"$project": {
                "_id": 0,
                "code": facet.code,
                "name": facet.name,
                "type": facet.type,
                "is_range": {"$toBool": True},
                "values": 1,
            }},
        ]
    }


def get_pipeline_to_retrieve_price_range(price_field_name: str = "price",
                                         product_filters: Optional[dict] = None) -> List[Dict]:
    final_pipeline = []
    if product_filters is not None:
        final_pipeline.append({
            "$match": product_filters
        })

    final_pipeline.append({
        "$bucketAuto": {
            "groupBy": f"${price_field_name}",
            "buckets": 1,
        }
    })

    return final_pipeline
