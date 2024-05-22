from src.config.database import db
from src.repositories.deal import DealRepository
from src.services.deal.deal_service import DealService

async def get_deal_service() -> DealService:
    deal_repository = DealRepository(db)
    deals_service = DealService(deal_repository)
    return deals_service
