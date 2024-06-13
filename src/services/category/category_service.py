from src.repositories.category import CategoryRepository
from src.schemes.category.params import CategoryListParams
from src.param_classes.category.category_filters import CategoryListFilters
from src.schemes.category.responses import CategoryListResponse


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def get_category_list_with_nearest_children_and_parent(self,
                                                                 params: CategoryListParams) -> CategoryListResponse:
        """
        Returns category list with nearest children and parent's data if parent_id is provided
        """
        filters = CategoryListFilters(parent_id=params.parent_id) \
            if params.parent_id is not None \
            else CategoryListFilters(level=0)

        category_lineage = await self.category_repository.get_categories_and_nearest_children(filters)
        return CategoryListResponse(**category_lineage)
