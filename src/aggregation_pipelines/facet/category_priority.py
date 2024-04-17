from typing import List, Dict
from bson import ObjectId

from src.query_utils.facet.category_priority import get_facet_category_priority


def get_pipeline_to_retrieve_facets_by_category_priority(category_ids: List[ObjectId],

                                                         facet_limit: int) -> List[Dict]:
    """
    Returns mongodb pipeline to return a list of facet codes.
    Each facet is associated with one or more categories, and the facet are returned
    in order of priority based on the category they are associated with. The priority
    is determined by the order of category IDs provided in the 'category_ids' list,
    with the first ID having the highest priority.
    """
    pipeline = [
        {
            "$match": {
                "categories": {
                    "$in": category_ids
                },
                "show_in_filters": True,
            }
        },
        {
            "$addFields": {
                "priority": {
                    "$switch": {
                        "branches": get_facet_category_priority(category_ids),
                        "default": len(category_ids)
                    },

                },
            }
        },
        {
            "$group": {
                "_id": "$code",
                "facet": {
                    "$first": "$$ROOT"
                },
            }
        },
        {
            "$replaceRoot": {"newRoot": "$facet"},
        },
        {
            "$sort": {
                "priority": 1,
                "code": 1,
            }
        },
        {
            "$limit": facet_limit
        },
        {
            "$project": {
                "priority": 0,
            }
        }
    ]

    return pipeline
