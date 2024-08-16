import json
from pathlib import Path

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

root_path = Path(__file__).parent.parent.parent

async def populate_category_data(db: AsyncIOMotorDatabase):
    """
    Creates categories in test environment
    """
    with open(root_path / 'test_data/test_data_categories.json', 'r') as f:
        categories = json.load(f)

    for category in categories:
        category["_id"] = ObjectId(category["_id"])
        category["parent_id"] = ObjectId(category["parent_id"]) if category["parent_id"] else None
        category["tree_id"] = ObjectId(category["tree_id"])

    category_collection = db.get_collection("categories")

    await category_collection.insert_many(categories)
