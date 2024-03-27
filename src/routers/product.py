import fastapi
from typing import Annotated

from src.schemes.product.filters import ProductFilters, ProductPaginationSettings
from src.schemes.product.get import FacetValuesResponse, ProductListResponse
from src.dependencies.service_dependencies.product import get_product_service
from src.services.product.product_service import ProductService

router = fastapi.APIRouter(
    prefix="/products",
    tags=["Products"]
)

FiltersDep = Annotated[ProductFilters, fastapi.Depends(ProductFilters)]
PaginationSettingsDep = Annotated[ProductPaginationSettings, fastapi.Depends(ProductPaginationSettings)]
ServiceDep = Annotated[ProductService, fastapi.Depends(get_product_service)]

@router.get("/facet-values", response_model=FacetValuesResponse)
async def get_products(filters: FiltersDep, service: ServiceDep):
    return await service.get_filtered_facet_values(filters)

@router.get("/", response_model=ProductListResponse)
async def get_products(filters: FiltersDep, pagination_settings: PaginationSettingsDep, service: ServiceDep):
    return await service.get_product_list(filters, pagination_settings)
