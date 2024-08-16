from bson import ObjectId
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase


class TestGetProductVariations:
    async def test_finding_variations_for_existing_product_having_siblings_should_pass(
            self, async_client: AsyncClient, test_database: AsyncIOMotorDatabase):
        """
        If the user wants to get variations for existing product,
        he should get the response HTTP 200 OK and product variations.
        """
        product_collection = test_database.get_collection("products")
        sellable_product_having_siblings = await product_collection.find_one({
            "parent": False,
            "stock": {"$gt": 0},
            "for_sale": True,
            "parent_id": {"$exists": True, "$ne": None},
        })
        product_id = sellable_product_having_siblings["_id"]

        response = await async_client.get(f"/api/v1/products/{product_id}/get-variations/")
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["variation_summary"]["variation_count"] > 0

    async def test_finding_variations_for_non_existing_product_should_fail(
            self, async_client: AsyncClient):
        """
        If the user wants to get variations for non-existing product, he should get the response HTTP 400 NOT FOUND.
        """
        random_object_id = ObjectId()

        response = await async_client.get(f"/api/v1/products/{random_object_id}/get-variations/")
        response_data = response.json()

        assert response.status_code == 404
        assert response_data["detail"] == "Specified product does not exist"

    async def test_finding_variations_for_existing_product_by_parent_id_should_pass(
            self, async_client: AsyncClient, test_database: AsyncIOMotorDatabase):
        """
        If the user wants to get variations for existing product by the product's parent_id, he can do that.
        """
        product_collection = test_database.get_collection("products")
        parent_product = await product_collection.find_one({
            "parent": True,
            "variation_theme": {"$exists": True, "$ne": None},
        })
        product_id = parent_product["_id"]

        response = await async_client.get(f"/api/v1/products/{product_id}/get-variations/")
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["variation_summary"]["variation_count"] > 0

    async def test_finding_variations_for_product_by_parent_id_should_fail(
            self, async_client: AsyncClient, test_database: AsyncIOMotorDatabase):
        """
        If the user wants to get variations for existing product which have no siblings,
        the user will get the response HTTP 400 BAD REQUEST.
        """
        product_collection = test_database.get_collection("products")
        sellable_product_having_no_siblings = await product_collection.find_one({
            "parent": False,
            "stock": {"$gt": 0},
            "for_sale": True,
            "parent_id": {"$exists": True, "$eq": None},
            "variation_theme": {"$exists": True, "$eq": None},
        })
        product_id = sellable_product_having_no_siblings["_id"]

        response = await async_client.get(f"/api/v1/products/{product_id}/get-variations/")
        response_data = response.json()

        assert response.status_code == 400
        assert response_data["detail"] == "Given product doesn't have variation theme"

