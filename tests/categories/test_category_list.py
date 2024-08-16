from bson import ObjectId
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase


class TestCategoryList:
    async def test_getting_category_list_without_specified_parent_id_should_return_root_categories(
            self, async_client: AsyncClient):
        response = await async_client.get("/api/v1/categories/")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["parent_data"] is None

    async def test_getting_category_list_with_specified_parent_id_should_return_nearest_child_categories(
            self, async_client: AsyncClient, test_database: AsyncIOMotorDatabase):
        category_collection = test_database.get_collection("categories")
        parent_category = await category_collection.find_one({
            "level": 0,
            "parent_id": None,
        })
        category_id = parent_category["_id"]

        response = await async_client.get("/api/v1/categories/", params={"parent_id": category_id})
        response_data = response.json()

        assert response.status_code == 200
        assert ObjectId(response_data["parent_data"]["_id"]) == category_id

    async def test_getting_category_list_with_non_existing_parent_should_return_nothing(self, async_client: AsyncClient):
        random_object_id = ObjectId()

        response = await async_client.get("/api/v1/categories/", params={"parent_id": str(random_object_id)})
        response_data = response.json()

        assert response_data["items"] == []
        assert response_data["parent_data"] is None
