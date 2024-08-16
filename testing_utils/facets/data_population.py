import json
from pathlib import Path

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

root_path = Path(__file__).parent.parent.parent

async def populate_facet_data(db: AsyncIOMotorDatabase):
    """
    Creates categories in test environment
    """
    with open(root_path / 'test_data/test_data_facets.json', 'r') as f:
        facets = json.load(f)

    for facet in facets:
        facet["_id"] = ObjectId(facet["_id"])
        categories = facet["categories"]
        if isinstance(categories, list):
            facet["categories"] = [ObjectId(category) for category in categories]

    facets_collection = db.get_collection("facets")

    await facets_collection.insert_many(facets)
