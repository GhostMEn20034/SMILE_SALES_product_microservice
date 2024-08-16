from httpx import AsyncClient


class TestDealList:
    async def test_getting_deal_list_should_pass(self, async_client: AsyncClient):
        response = await async_client.get("/api/v1/deals/")

        assert response.status_code == 200
