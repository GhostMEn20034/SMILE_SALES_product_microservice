def get_pipeline_to_get_display_name():
    return {
        "$switch": {
            "branches": [
                # Convert integer, decimal, or double to string
                # and concatenate it with a unit of measurement if it presents.
                {
                    "case": {"$in": ["$facet_type", ['decimal', 'integer']]},
                    "then": {
                        "$trim": {
                            "input": {
                                "$concat": [
                                    {"$toString": "$_id.value"}, " ", {"$ifNull": ["$_id.unit", ""]}]
                            }
                        }
                    }
                },
                # Since list can have only string items,
                # and we unwind this list before switch-case, we include "list" to "case"
                {
                    "case": {"$in": ["$facet_type", ['string', 'list']]},
                    "then": {
                        "$trim": {
                            "input": {
                                "$concat": ["$_id.value", " ", {"$ifNull": ["$_id.unit", ""]}]
                            }}
                    }
                },
                # If value is bivariate , it means is object. Concatenate value.x, " x ", value.y.
                {
                    "case": {"$eq": ["$facet_type", "bivariate"]},
                    "then": {
                        "$trim": {
                            "input": {
                                "$concat": [
                                    {"$toString": "$_id.value.x"}, " x ",
                                    {"$toString": "$_id.value.y"}, " ",
                                    {"$ifNull": ["$_id.unit", ""]},
                                ]
                            }
                        }
                    }
                },
                # If value is trivariate , it means is object. Concatenate value.x, " x ", value.y, " x ", value.z
                {
                    "case": {"$eq": ["$facet_type", "trivariate"]},
                    "then": {"$trim": {
                        "input": {
                            "$concat": [
                                {"$toString": "$_id.value.x"}, " x ",
                                {"$toString": "$_id.value.y"}, " x ",
                                {"$toString": "$_id.value.z"}, " ",
                                {"$ifNull": ["$_id.unit", ""]},
                            ]
                        }
                    }
                    }
                },
            ]
        }
    }


def get_pipeline_to_retrieve_facet_values(code: str, match_statement: dict):
    """
    Returns the pipeline to retrieve the facet values
    :param code: The code of the facet
    :param match_statement: The pipeline stage to filtering products from which values are given
    """
    return {
        code: [
            {"$match": match_statement},
            {"$unwind": "$attrs"},
            {"$unwind": "$attrs.value"},
            {"$match": {"attrs.code": code}},
            {"$group": {"_id": {"code": "$attrs.code", "value": "$attrs.value", "unit": "$attrs.unit"},
                        "name": {"$first": "$attrs.name"},
                        "facet_type": {"$first": "$attrs.type"},
                        "explanation": {"$first": "$attrs.explanation"},
                        "count": {"$sum": 1}}
             },

            {"$project": {
                "code": "$_id.code",
                "value": "$_id.value",
                "unit": "$_id.unit",
                "count": 1,
                "display_name": get_pipeline_to_get_display_name(),
                "name": "$name",
                "explanation": "$explanation",
            }},
            {"$sort": {"value": 1, "unit": 1, "code": 1}},
            {"$group": {"_id": "$_id.code",
                        "values": {"$push": {
                            "value": "$_id.value",
                            "unit": "$_id.unit",
                            "count": "$count",
                            "display_name": "$display_name",
                        }},
                        "name": {"$first": "$name"},

                        "explanation": {"$first": "$explanation"}
                        }},
            {"$project": {
                "_id": 0,
                "code": "$_id",
                "name": "$name",
                "explanation": "$explanation",
                "values": "$values"
            }}
        ]
    }


def get_pipeline_to_retrieve_price_range():

    facet_pipeline = [
        {
            "$bucketAuto": {
                "groupBy": "$price",
                "buckets": 1,
            }
        }
    ]
    return facet_pipeline
