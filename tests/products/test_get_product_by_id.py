from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from httpx import AsyncClient


class TestGetProductById:
    async def test_finding_product_with_existing_id_should_pass(self, async_client: AsyncClient,
                                                            test_database: AsyncIOMotorDatabase):
        """
        If the user finds the product with an existing id, it should return it.
        """
        product_collection = test_database.get_collection("products")
        sellable_product = await product_collection.find_one({
            "parent": False,
            "stock": {"$gt": 0},
            "for_sale": True,
        })
        product_id = sellable_product["_id"]

        response = await async_client.get(f"/api/v1/products/{product_id}")
        response_data = response.json()

        assert response.status_code == 200
        assert ObjectId(response_data["item"]["_id"]) == product_id

    async def test_finding_product_with_non_existing_id_should_fail(self, async_client: AsyncClient):
        """
        If the user finds the product with non-existing id, it should return HTTP 404 NOT FOUND.
        """
        random_object_id = ObjectId()

        response = await async_client.get(f"/api/v1/products/{random_object_id}")
        response_data = response.json()

        assert response.status_code == 404
        assert response_data["detail"] == "Product with the specified ID does not exist"


    async def test_finding_parent_product_should_fail(self, async_client: AsyncClient,
                                                      test_database: AsyncIOMotorDatabase):
        """
        If the user trying to find parent product (It cannot be sellable),
        he should get the response with HTTP 400 BAD REQUEST.
        """
        product_collection = test_database.get_collection("products")
        parent_product = await product_collection.find_one({
            "parent": True,
        })
        product_id = parent_product["_id"]

        response = await async_client.get(f"/api/v1/products/{product_id}")
        response_data = response.json()

        assert response.status_code == 400
        assert response_data["detail"] == "Parent product cannot be sold"



