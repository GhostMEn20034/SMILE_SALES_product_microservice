import asyncio
from typing import AsyncGenerator
import pytest
import pytest_asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import AsyncClient

from src.main import app
from src.config.database import client
from testing_utils.deals.data_population import populate_deal_data
from testing_utils.facets.data_population import populate_facet_data
from testing_utils.products.data_population import populate_product_data
from testing_utils.categories.data_population import populate_category_data


@pytest.fixture(scope="session", autouse=True)
async def initialize_cache():
    # Initialize the FastAPICache with an in-memory backend
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_database(event_loop):
    # Replace the database connection with the test database
    test_db = client.get_database("test_db")

    await populate_category_data(test_db)
    await populate_facet_data(test_db)
    await populate_product_data(test_db)
    await populate_deal_data(test_db)

    yield test_db

    # Teardown: clean up the test database after tests are done
    client.drop_database(test_db)

@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
