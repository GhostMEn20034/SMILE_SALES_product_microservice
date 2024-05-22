from typing import Dict, List

from src.aggregation_pipelines.base.pagination_pipelines import get_pagination_to_skip_items
from src.schemes.deal.pagination_settings import DealPaginationSettings


def get_pipeline_to_retrieve_list_of_deals(pagination_settings: DealPaginationSettings) -> List[Dict]:
    pipeline = [
        {"$match": {
            "is_visible": True,
            "parent_id": None,
        }},
        {"$facet": {
            "items": [
                *get_pagination_to_skip_items(pagination_settings.page, pagination_settings.page_size),
                {"$sort": {
                    "modified_at": -1,
                }},
                {"$project": {
                    "name": 1,
                    "is_parent": 1,
                    "parent_id": 1,
                    "query_string": 1,
                    "button_text": 1,
                    "image": 1,
                }},
            ],
            "count": [
                {
                    "$count": "count",
                }
            ],
        }},
        {"$unwind": "$count"},
        {"$project": {
            "items": 1,
            "count": "$count.count",
        }},
    ]

    return pipeline
