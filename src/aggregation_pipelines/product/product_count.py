from typing import Dict, List


def build_product_count_by_category_pipeline() -> List[Dict]:
    """
    Constructs a pipeline to retrieve product count grouped by category.
    """
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "count": {"$sum": 1},
            }
        },
        {"$project": {
            "_id": 0,
            "category_id": "$_id",
            "count": 1,
        }},
        {
            "$sort": {
                "count": -1,
            }
        }
    ]

    return pipeline


def build_product_count_by_category_with_join(category_collection_name: str = "categories") -> List[Dict]:
    """
    Constructs a pipeline to retrieve product count with joined category data.
    """
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "count": {"$sum": 1},
            }
        },
        {"$lookup": {
            "from": category_collection_name,
            "localField": "_id",
            "foreignField": "_id",
            "as": "category_data",
            "pipeline": [
                {"$project": {
                    "name": 1,
                }},
            ]
        }},
        {"$unwind": "$category_data"},
        {"$project": {
            "_id": 1,
            "name": "$category_data.name",
            "count": 1,
        }},
    ]

    return pipeline
