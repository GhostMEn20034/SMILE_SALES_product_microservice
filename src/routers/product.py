import fastapi
from typing import Annotated
from fastapi_cache.decorator import cache

from src.schemes.base.pyobject_id import PyObjectId
from src.schemes.product.filters.product_list import ProductFilters, ProductPaginationSettings
from src.schemes.product.responses.get_variations import GetVariationsResponse
from src.schemes.product.responses.facet_values import FacetValuesResponse
from src.schemes.product.responses.product_list import ProductListResponse
from src.schemes.product.responses.product_details import ProductDetailsResponse
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
@cache(expire=60 * 30, namespace="products") # Cache the response for 30 minutes
async def get_facet_values(filters: FiltersDep, service: ServiceDep) -> FacetValuesResponse:
    ProductValidator.validate_product_filters(filters)
    return await service.get_filtered_facet_values(filters)


@router.get("/", response_model=ProductListResponse)
@cache(expire=60 * 30, namespace="products") # Cache the response for 30 minutes
async def get_product_list(filters: FiltersDep, pagination_settings: PaginationSettingsDep,
                           service: ServiceDep) -> ProductListResponse:
    ProductValidator.validate_product_filters(filters)
    return await service.get_product_list(filters, pagination_settings)


@router.get("/{product_id}/get-variations/", response_model=GetVariationsResponse)
@cache(expire=60 * 30, namespace="products") # Cache the response for 30 minutes
async def get_product_variations(product_id: PyObjectId, service: ServiceDep) -> GetVariationsResponse:
    return await service.get_product_variations_and_options(product_id)


@router.get("/{product_id}", response_model=ProductDetailsResponse)
@cache(expire=60 * 10, namespace="products") # Cache the response for 10 minutes
async def get_product(product_id: PyObjectId, service: ServiceDep) -> ProductDetailsResponse:
    return await service.get_product_by_id(product_id)
