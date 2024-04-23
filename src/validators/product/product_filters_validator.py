from src.schemes.product.filters.product_list import ProductFilters

class ProductFiltersValidator:
    """
    Class to validate an instance of ProductFilters
    """

    def __init__(self, product_filters_instance: ProductFilters):
        self.product_filters: ProductFilters = product_filters_instance

    def validate(self):
        """
        Validates the availability of category or query search.
        Returns True if at least one of them is not None, otherwise False.
        """
        return self.product_filters.category is not None or \
               self.product_filters.q is not None
