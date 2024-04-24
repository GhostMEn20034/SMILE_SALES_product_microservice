def get_string_and_list_branches(type_field_name: str, value_field_name: str,
                                 unit_field_name: str, list_is_unwinded: bool):
    if list_is_unwinded:
        # Since list can have only string items,
        # and we unwind this list before switch-case, we include "list" to "case"
        return [{
            "case": {"$in": [f"${type_field_name}", ['string', 'list']]},
            "then": {
                "$trim": {
                    "input": {
                        "$concat": [f"${value_field_name}", " ", {"$ifNull": [f"${unit_field_name}", ""]}]
                    }}
            }
        }, ]

    # If list is not unwinded, then we create separate branch for list type
    return [
        {
            "case": {"$eq": [f"${type_field_name}", 'string']},
            "then": {
                "$trim": {
                    "input": {
                        "$concat": [f"${value_field_name}", " ", {"$ifNull": [f"${unit_field_name}", ""]}]
                    }}
            }
        },
        {
            "case": {"$eq": [f"${type_field_name}", 'list']},
            "then": {
                "$trim": {
                    "input": {
                        "$reduce": {
                            "input": f"${value_field_name}",
                            "initialValue": "",
                            'in': {
                                '$concat': [
                                    '$$value',
                                    {'$cond': [{'$eq': ['$$value', '']}, '', ', ']},
                                    {"$toString": "$$this"}
                                ]
                            }
                        }
                    }}
            }
        },
    ]



def get_facets_display_name_expression(facet_type: str, attribute_object_name: str = "_id"):
    """
    returns an expression to evaluate a display name based on a facet type.
    :param facet_type: The type of facet to be displayed.
    :param attribute_object_name: The name of the attribute object
    """
    # Convert integer, decimal, or double to string
    # and concatenate it with a unit of measurement if it presents.
    if facet_type in ['decimal', 'integer']:
        display_name = {
            "$trim": {
                "input": {
                    "$concat": [
                        {"$toString": f"${attribute_object_name}.value"},
                        " ",
                        {"$ifNull": [f"${attribute_object_name}.unit", ""]}]
                }
            }
        }
    # Since list can have only string items,
    # and we unwind this list before getting display name, we include "list" to the condition
    elif facet_type in ['string', 'list']:
        display_name = {
            "$trim": {
                "input": {
                    "$concat": [
                        f"${attribute_object_name}.value",
                        " ",
                        {"$ifNull": [f"${attribute_object_name}.unit", ""]}
                    ]
                }}
        }
    # If value is bivariate , it means is object. Concatenate (value.x, " x ", value.y)
    elif facet_type == 'bivariate':
        display_name = {
            "$trim": {
                "input": {
                    "$concat": [
                        {"$toString": f"${attribute_object_name}.value.x"}, " x ",
                        {"$toString": f"${attribute_object_name}.value.y"}, " ",
                        {"$ifNull": [f"${attribute_object_name}.unit", ""]},
                    ]
                }
            }
        }
    # If value is trivariate , it means is object. Concatenate (value.x, " x ", value.y, " x ", value.z).
    elif facet_type == 'trivariate':
        display_name = {
            "$trim": {
                "input": {
                    "$concat": [
                        {"$toString": f"${attribute_object_name}.value.x"}, " x ",
                        {"$toString": f"${attribute_object_name}.value.y"}, " x ",
                        {"$toString": f"${attribute_object_name}.value.z"}, " ",
                        {"$ifNull": [f"${attribute_object_name}.unit", ""]},
                    ]
                }
            }
        }
    # In other cases we return the same display name as in case with the string
    else:
        display_name = {
            "$trim": {
                "input": {
                    "$concat": [
                        f"${attribute_object_name}.value",
                        " ",
                        {"$ifNull": [f"${attribute_object_name}.unit", ""]}
                    ]
                }}
        }

    return display_name


def get_facets_display_name_switch_case(type_field_name: str = "facet_type",
                                        value_field_name: str = "attr.value",
                                        unit_field_name: str = "attr.unit",
                                        list_is_unwinded: bool = False,
                                        ):
    """
    This function returns a switch-case operator that computes a display name based on a facet type.
    :param type_field_name: The field name where the facet type is stored.
    :param value_field_name: The name of the attribute's / facet's value field.
    :param unit_field_name: The name of the attribute's / facet's unit field.
    :param list_is_unwinded: Boolean to determine
    if a facet's value is unwinded ($unwind operator was applied to facet's value).
    """
    string_and_list_branches = get_string_and_list_branches(type_field_name, value_field_name,
                                                            unit_field_name, list_is_unwinded)

    return {
        "$switch": {
            "branches": [
                # Convert integer, decimal, or double to string
                # and concatenate it with a unit of measurement if it presents.
                {
                    "case": {"$in": [f"${type_field_name}", ['decimal', 'integer']]},
                    "then": {
                        "$trim": {
                            "input": {
                                "$concat": [
                                    {"$toString": f"${value_field_name}"}, " ",
                                    {"$ifNull": [f"${unit_field_name}", ""]}]
                            }
                        }
                    }
                },
                # Since list can have only string items,
                # and we unwind this list before switch-case, we include "list" to "case"
                *string_and_list_branches,
                # If value is bivariate , it means is object. Concatenate value.x, " x ", value.y.
                {
                    "case": {"$eq": [f"${type_field_name}", "bivariate"]},
                    "then": {
                        "$trim": {
                            "input": {
                                "$concat": [
                                    {"$toString": f"${value_field_name}.x"}, " x ",
                                    {"$toString": f"${value_field_name}.y"}, " ",
                                    {"$ifNull": [f"${unit_field_name}", ""]},
                                ]
                            }
                        }
                    }
                },
                # If value is trivariate , it means is object. Concatenate value.x, " x ", value.y, " x ", value.z
                {
                    "case": {"$eq": [f"${type_field_name}", "trivariate"]},
                    "then": {"$trim": {
                        "input": {
                            "$concat": [
                                {"$toString": f"${value_field_name}.x"}, " x ",
                                {"$toString": f"${value_field_name}.y"}, " x ",
                                {"$toString": f"${value_field_name}.z"}, " ",
                                {"$ifNull": [f"${unit_field_name}", ""]},
                            ]
                        }
                    }
                    }
                },
            ],
            'default': "Hello"
        }
    }
