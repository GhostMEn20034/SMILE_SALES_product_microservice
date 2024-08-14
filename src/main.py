from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.lifespan import lifespan
from src.config.settings import settings

from src.routers.search_term import router as search_term_router
from src.routers.product import router as product_router
from src.routers.deal import router as deal_router
from src.routers.event import router as event_router
from src.routers.category import router as category_router


app = FastAPI(lifespan=lifespan)

origins = settings.allowed_origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_term_router, prefix='/api/v1')
app.include_router(product_router, prefix='/api/v1')
app.include_router(deal_router, prefix='/api/v1')
app.include_router(event_router, prefix='/api/v1')
app.include_router(category_router, prefix='/api/v1')


@app.get("/ping")
async def ping() -> dict:
    return {"response": "pong"}