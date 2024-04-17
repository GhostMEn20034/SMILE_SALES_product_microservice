def get_facets_display_name(facet_type: str):
    # Convert integer, decimal, or double to string
    # and concatenate it with a unit of measurement if it presents.
    if facet_type in ['decimal', 'integer']:
        display_name = {
            "$trim": {
                "input": {
                    "$concat": [
                        {"$toString": "$_id.value"}, " ", {"$ifNull": ["$_id.unit", ""]}]
                }
            }
        }
    # Since list can have only string items,
    # and we unwind this list before getting display name, we include "list" to the condition
    elif facet_type in ['string', 'list']:
        display_name = {
            "$trim": {
                "input": {
                    "$concat": ["$_id.value", " ", {"$ifNull": ["$_id.unit", ""]}]
                }}
        }
    # If value is bivariate , it means is object. Concatenate (value.x, " x ", value.y)
    elif facet_type == 'bivariate':
        display_name = {
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
    # If value is trivariate , it means is object. Concatenate (value.x, " x ", value.y, " x ", value.z).
    elif facet_type == 'trivariate':
        display_name = {
            "$trim": {
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
    # In other cases we return the same display name as in case with the string
    else:
        display_name = {
            "$trim": {
                "input": {
                    "$concat": ["$_id.value", " ", {"$ifNull": ["$_id.unit", ""]}]
                }}
        }

    return display_name
