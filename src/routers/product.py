import fastapi
from typing import Annotated

from src.schemes.base.pyobject_id import PyObjectId
from src.schemes.product.filters.product_list import ProductFilters, ProductPaginationSettings
from src.schemes.product.responses.get_variations import GetVariationsResponse
from src.schemes.product.responses.facet_values import FacetValuesResponse
from src.schemes.product.responses.product_list import ProductListResponse
from src.dependencies.service_dependencies.product import get_product_service
from src.services.product.product_service import ProductService
from src.services.product.product_validator import ProductValidator

router = fastapi.APIRouter(
    prefix="/products",
    tags=["Products"]
)

FiltersDep = Annotated[ProductFilters, fastapi.Depends(ProductFilters)]
PaginationSettingsDep = Annotated[ProductPaginationSettings, fastapi.Depends(ProductPaginationSettings)]
ServiceDep = Annotated[ProductService, fastapi.Depends(get_product_service)]


@router.get("/facet-values", response_model=FacetValuesResponse)
async def get_facet_values(filters: FiltersDep, service: ServiceDep):
    ProductValidator.validate_product_filters(filters)
    return await service.get_filtered_facet_values(filters)

@router.get("/", response_model=ProductListResponse)
async def get_products_list(filters: FiltersDep, pagination_settings: PaginationSettingsDep, service: ServiceDep):
    ProductValidator.validate_product_filters(filters)
    return await service.get_product_list(filters, pagination_settings)

@router.get("/{product_id}/get-variations/", response_model=GetVariationsResponse)
async def get_product_variations(product_id: PyObjectId, service: ServiceDep):
    return await service.get_product_variations_and_options(product_id)

