from typing import List, Union, Dict

from src.schemes.facet.base import RangeValue, Facet
from src.schemes.facet.facet_metadata import FacetMetadataItem


class FacetMetadataProvider:
    """
    Provides metadata about a facet such as all facet codes, or display name fields for range values etc.
    """

    def __init__(self, facets: List[Facet]):
        self.facets = facets

    @staticmethod
    def get_range_value_to_display_name_mapping(range_values: List[RangeValue]) -> Dict[Union[float, int], str]:
        """
        Creates a mapping between gteq (Greater Than Equal) field in range value to display name
        """
        gte_field_to_display_name_mapping = {
            item.gteq: item.display_name for item in range_values
        }
        return gte_field_to_display_name_mapping

    def get_facet_metadata(self) -> Dict[str, FacetMetadataItem]:
        facet_metadata = {}
        for facet in self.facets:
            range_value_to_display_name_mapping = self.get_range_value_to_display_name_mapping(
                facet.range_values
            ) if facet.is_range else None

            facet_metadata_item = FacetMetadataItem(
                name=facet.name,
                range_to_display_name=range_value_to_display_name_mapping
            )
            facet_metadata[facet.code] = facet_metadata_item

        return facet_metadata
