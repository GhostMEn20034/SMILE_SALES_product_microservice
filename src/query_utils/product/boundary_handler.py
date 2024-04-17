from src.config.constants import MAX_SAFE_INTEGER


class BoundaryHandler:
    """
    Responsible for creation a part of aggregation query that assigns
    fields to the document based on the boundary value
    """
    def __init__(self, boundary_item_field_name="_id"):
        """
        :param boundary_item_field_name: field name of each value of $bucket operator result
        """
        self._boundary_item_field_name = boundary_item_field_name

    def get_boundary_value(self, boundary_to_range_mapping: dict):
        """
        Returns MongoDB's switch-case query that calculates a 'value' field for facet values.
        """
        # Create a list to hold the switch-case branches
        branches = [
            {
                "case": {"$eq": [f"${self._boundary_item_field_name}", boundary]},
                "then": value
            } for boundary, value in boundary_to_range_mapping.items()
        ]

        # Construct and return the switch-case query
        return {
            "$switch": {
                "branches": branches,
                "default": {"gteq": 0, "ltn": MAX_SAFE_INTEGER}
            }
        }

    def get_boundary_display_name(self, boundary_to_display_name_mapping: dict):
        """
        Returns MongoDB's switch-case query that calculates a 'display_name' field for facet values.
        """
        # Use a list comprehension to create the switch-case branches
        branches = [
            {
                "case": {"$eq": [f"${self._boundary_item_field_name}", boundary]},
                "then": display_name
            } for boundary, display_name in boundary_to_display_name_mapping.items()
        ]

        # Return the switch-case query with a default case
        return {
            "$switch": {
                "branches": branches,
                "default": "Other"
            }
        }
