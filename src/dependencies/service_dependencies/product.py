from src.config.database import db
from src.repositories.product import ProductRepository
from src.repositories.category import CategoryRepository
from src.repositories.facet import FacetRepository
from src.repositories.search_term import SearchTermRepository
from src.services.product.product_service import ProductService
from src.services.search_term.search_term_service import SearchTermService


async def get_product_service() -> ProductService:
    product_repository = ProductRepository(db)
    category_repository = CategoryRepository(db)
    facet_repository = FacetRepository(db)
    search_term_repository = SearchTermRepository(db)
    search_term_service = SearchTermService(search_term_repository)

    return ProductService(product_repository, category_repository,
                          facet_repository, search_term_service)
