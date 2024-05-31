from typing import Dict, List

from src.schemes.event.pagination_settings import EventPaginationSettings
from src.aggregation_pipelines.base.pagination_pipelines import get_pagination_to_skip_items


def get_pipeline_to_retrieve_event_list(filters: dict,
                                        pagination_settings: EventPaginationSettings) -> List[Dict]:
    pipeline = [
        {"$match": filters},
        {"$facet": {
            "items": [
                {"$sort": {
                    "start_date": -1,
                }},
                *get_pagination_to_skip_items(pagination_settings.page, pagination_settings.page_size),
                {"$project": {
                    "discounted_products": 0,
                    "description": 0,
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