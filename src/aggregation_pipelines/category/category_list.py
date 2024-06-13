from typing import Dict, List

from src.param_classes.category.category_filters import CategoryListFilters

def build_pipeline_to_retrieve_category_lineage(filters: CategoryListFilters, collection_name: str) -> List[Dict]:
    aggregations = {
        "items": [
            {"$match": filters.model_dump(exclude_none=True)},
            {"$graphLookup": {
                "from": collection_name,
                "startWith": "$_id",
                "connectFromField": "_id",
                "connectToField": "parent_id",
                "as": "nearest_children",
                "maxDepth": 0,
            }},
            {"$project": {
               "_id": 1,
               "name": 1,
                "nearest_children": {
                    "_id": 1,
                    "name": 1,
                },
            }},
        ],
    }

    final_projection = {
        "items": 1
    }

    if filters.parent_id:
        aggregations["parent_data"] = [
            {"$match": {
                "_id": filters.parent_id,
            }},
            {"$project": {
               "_id": 1,
               "name": 1,
            }},
        ]

        final_projection["parent_data"] = {
            "$arrayElemAt": ["$parent_data", 0]
        }

    pipeline = [
        {"$facet": aggregations},
        {"$project": final_projection}
    ]

    return pipeline