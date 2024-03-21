from typing import Dict, List


class FacetValueResults:
    """
    Encapsulates the result of get_facet_values method in ProductRepository
    """
    def __init__(self, facet_values: List[Dict], price_range_facet: Dict):
        self.facet_values = facet_values
        self.price_range_facet = price_range_facet
