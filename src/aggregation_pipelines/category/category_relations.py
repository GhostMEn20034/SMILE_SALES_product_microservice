from bson import ObjectId


def get_category_relations(category_id: ObjectId, collection_name: str, auto_defined: bool = False):
    """
    Returns a pipeline to get category's children on 1 level deeper and ancestors
    :param category_id: ID of the category to get children and ancestors.
    :param collection_name: Name of the MongoDb collection to work with categories.
    :param auto_defined: Defines whether current category is defined automatically or specified manually.
    Required for response model further processing.
    """
    pipeline = [
        {"$match": {"_id": category_id}},
        {
            "$facet": {
                "current": [
                    {"$project": {
                        "name": 1,
                        "auto_defined": {"$toBool": auto_defined},
                    }}

                ],
                "ancestors": [
                    {
                        "$graphLookup": {
                            "from": collection_name,
                            "startWith": "$parent_id",
                            "connectFromField": "parent_id",
                            "connectToField": "_id",
                            "as": "ancestors",
                            "depthField": "depth",
                        }
                    },
                    {
                        "$project": {
                            "ancestors": {
                                "$sortArray": {
                                    "input": "$ancestors",
                                    "sortBy": {"depth": -1}
                                }
                            }
                        }
                    }
                ],
                "all_children": [
                    {
                        "$graphLookup": {
                            "from": collection_name,
                            "startWith": "$_id",
                            "connectFromField": "_id",
                            "connectToField": "parent_id",
                            "as": "all_children",
                            "depthField": "depth",
                        }
                    }
                ],
            }
        },
        {
            "$project": {
                "current": {"$arrayElemAt": ["$current", 0]},
                "ancestors": {"$arrayElemAt": ["$ancestors.ancestors", 0]},
                "all_children": {"$arrayElemAt": ["$all_children.all_children", 0]},
            }
        },
        {"$addFields": {
            "nearest_children": {
                "$filter": {
                    "input": "$all_children",
                    "as": "child",
                    "cond": {"$eq": ["$$child.depth", 0]}
                }
            }
        }},
    ]

    return pipeline


def get_category_children_pipeline(category_id: ObjectId, collection_name: str):
    """
    Pipeline for getting all category's children
    """
    pipeline = [
        {"$match": {"_id": category_id}},
        {
            "$graphLookup": {
                "from": collection_name,
                "startWith": "$_id",
                "connectFromField": "_id",
                "connectToField": "parent_id",
                "as": "children",
                "depthField": "depth",
            }
        },
        {"$unwind": "$children"},
        {
            "$replaceRoot": {"newRoot": "$children"}
        }
    ]

    return pipeline
