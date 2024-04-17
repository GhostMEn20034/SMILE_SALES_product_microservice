from typing import Dict, List, Union

from src.schemes.product.facet_value_filters import FacetFilterObject, FacetOption, RangeFacetValue
from src.schemes.product.attributes import Trivariate, Bivariate


class ChosenFacetFilterBuilder:
    """
    A utility class for constructing filter criteria based on user-selected facets.

    This class takes user input regarding various facets of a selection process and
    generates a set of filters that can be applied to a dataset to narrow down the results
    according to the user's preferences.
    """
    def __init__(self, chosen_facets: Dict[str, FacetFilterObject]):
        self.chosen_facets = chosen_facets
        self.attribute_field_name: str = 'attrs'

    @staticmethod
    def dump_facet_option_value(value: Union[Trivariate, Bivariate, RangeFacetValue, float, int, str]):
        if isinstance(value, (float, int, str)):
            return value
        else:
            return value.model_dump()

    def _build_regular_facet_filter(self, facet_code: str, facet_options: List[FacetOption]):
        facet_filters = []
        for facet_option in facet_options:
            facet_filters.append(
                {"code": facet_code,
                 "value": self.dump_facet_option_value(facet_option.value),
                 "unit": facet_option.unit}
            )

        return {self.attribute_field_name: {"$elemMatch": {"$or": facet_filters}}}

    def _build_range_facet_filter(self, facet_code: str, facet_options: List[FacetOption]):
        facet_filters = []
        for facet_option in facet_options:
            value_filter = {"$gte": facet_option.value.gteq}
            if facet_option.value.ltn is not None:
                value_filter["$lt"] = facet_option.value.ltn

            facet_filters.append(
                {"code": facet_code,
                 "value": value_filter,
                 }
            )

        return {self.attribute_field_name: {"$elemMatch": {"$or": facet_filters}}}

    def build_filters(self):
        facet_filters = []
        for facet_code, facet_object in self.chosen_facets.items():
            if len(facet_object.values) > 0:

                if not facet_object.is_range:
                    facet_filters.append(
                        self._build_regular_facet_filter(facet_code, facet_object.values)
                    )
                else:
                    facet_filters.append(
                        self._build_range_facet_filter(facet_code, facet_object.values)
                    )

        return facet_filters
