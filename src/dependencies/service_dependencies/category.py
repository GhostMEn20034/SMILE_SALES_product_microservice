from src.config.database import db
from src.repositories.category import CategoryRepository
from src.services.category.category_service import CategoryService


async def get_category_service() -> CategoryService:
    category_repository: CategoryRepository = CategoryRepository(db)
    return CategoryService(category_repository)