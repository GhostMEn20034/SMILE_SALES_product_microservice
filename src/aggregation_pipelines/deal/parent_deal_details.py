from typing import List, Dict

from src.param_classes.deal.parent_deal_details import ParentDealDetailsParams

def get_pipeline_to_retrieve_parent_deal_details(params: ParentDealDetailsParams) -> List[Dict]:
    deal_projection = {
        "name": 1,
        "is_parent": 1,
        "parent_id": 1,
        "query_string": 1,
        "button_text": 1,
        "image": 1,
    }

    pipeline = [
        {"$match": {
            "_id": params.deal_id,
        }},
        {"$lookup": {
            "from": params.collection_name,
            "localField": "_id",
            "foreignField": "parent_id",
            "as": "children",
            "pipeline": [
                {"$match": {
                    "is_visible": True,
                }},
                {"$sort": {
                    "modified_at": -1,
                }},
                {"$project": deal_projection},
            ],
        }},
        {"$project": {
            **deal_projection,
            "description": 1,
            "children": 1,
        }},
    ]

    return pipeline
