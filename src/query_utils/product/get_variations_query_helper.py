from src.query_utils.product.facet_values_display_name import get_facets_display_name_switch_case


class ProductVariationsQueryHelper:
    """
    Helper class to create a mongodb pipeline for product variations' related data
    """
    def __init__(self, attr_codes: list[str], attr_object_key_name: str = "_id"):
        self.attr_codes = attr_codes
        self.attr_group_key_name: str = attr_object_key_name

    def get_group_keys(self):
        group_keys = {}
        for attr in self.attr_codes:
            group_keys[attr] = f"$values.{attr}"

        return group_keys

    def get_display_name_for_each_attr_code(self):
        display_name_fields = {}
        for attr in self.attr_codes:
            display_name = get_facets_display_name_switch_case(
                f"{self.attr_group_key_name}.{attr}.type",
                f"{self.attr_group_key_name}.{attr}.value",
                f"{self.attr_group_key_name}.{attr}.unit"
            )
            display_name_fields[f"{self.attr_group_key_name}.{attr}.display_name"] = display_name

        return display_name_fields

    def get_projection_to_exclude_redundant_fields(self):
        redundant_fields = {}

        for attr in self.attr_codes:
            redundant_fields[f"{self.attr_group_key_name}.{attr}.display_name"] = 0
            redundant_fields[f"{self.attr_group_key_name}.{attr}.type"] = 0

        return redundant_fields

    def get_sort_keys_for_attributes(self, asc: bool = True, attr_group_key_name: str = None):
        group_key_name = attr_group_key_name if attr_group_key_name is not None else self.attr_group_key_name
        sort_keys = {}
        for attr in self.attr_codes:
            sort_keys[f"{group_key_name}.{attr}.unit"] = int(asc)
            sort_keys[f"{group_key_name}.{attr}.value"] = int(asc)

        return sort_keys

