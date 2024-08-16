from bson import ObjectId
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase


class TestDealDetails:
    async def test_getting_parent_deal_with_existing_id_should_pass(
            self, async_client: AsyncClient, test_database: AsyncIOMotorDatabase):
        deal_collection = test_database.get_collection("deals")
        parent_deal = await deal_collection.find_one({
            "is_parent": True,
            "is_visible": True,
        })
        deal_id = parent_deal["_id"]

        response = await async_client.get(f"/api/v1/deals/{deal_id}")
        response_data = response.json()

        assert response.status_code == 200
        assert ObjectId(response_data["item"]["_id"]) == deal_id

    async def test_getting_parent_deal_with_non_existing_id_should_fail(self, async_client: AsyncClient):
        random_object_id = ObjectId()

        response = await async_client.get(f"/api/v1/deals/{random_object_id}")
        response_data = response.json()

        assert response.status_code == 404
        assert response_data["detail"] == "The deal with the specified criteria does not exist"
