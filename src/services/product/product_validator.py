from fastapi.exceptions import HTTPException
from fastapi import status

from src.schemes.product.filters.product_list import ProductFilters
from src.validators.product.product_filters_validator import ProductFiltersValidator


class ProductValidator:
    """
    Stores methods that validates product-related data.
    """
    @staticmethod
    def validate_product_filters(product_filters: ProductFilters):
        product_filters_validator = ProductFiltersValidator(product_filters)
        if not product_filters_validator.validate():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Category or query string must specified"}
            )
