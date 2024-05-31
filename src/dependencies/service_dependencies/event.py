from src.config.database import db
from src.repositories.event import EventRepository
from src.repositories.product import ProductRepository
from src.services.event.event_service import EventService


async def get_event_service() -> EventService:
    event_repository = EventRepository(db)
    product_repository = ProductRepository(db)
    event_service = EventService(event_repository, product_repository)
    return event_service