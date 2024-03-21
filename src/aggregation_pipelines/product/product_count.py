def get_pipeline_to_retrieve_product_count_by_category():

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
