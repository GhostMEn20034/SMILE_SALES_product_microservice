import fastapi
from typing import Annotated

from src.dependencies.service_dependencies.category import get_category_service
from src.services.category.category_service import CategoryService
from src.schemes.category.responses import CategoryListResponse
from src.schemes.category.params import CategoryListParams

router = fastapi.APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


ServiceDep = Annotated[CategoryService, fastapi.Depends(get_category_service)]
CategoryListFiltersDep = Annotated[CategoryListParams, fastapi.Depends(CategoryListParams)]


@router.get("/", response_model=CategoryListResponse)
async def get_category_list(filters: CategoryListFiltersDep, service: ServiceDep):
    return await service.get_category_list_with_nearest_children_and_parent(filters)