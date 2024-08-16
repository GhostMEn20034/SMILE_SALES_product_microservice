import json
from pathlib import Path

from bson import ObjectId, Decimal128
from dateutil.parser import parse
from motor.motor_asyncio import AsyncIOMotorDatabase

root_path = Path(__file__).parent.parent.parent

async def populate_deal_data(db: AsyncIOMotorDatabase):
    """
    Creates categories in test environment
    """
    with open(root_path / 'test_data/test_data_deals.json', 'r') as f:
        deals = json.load(f)

    for deal in deals:
        deal["_id"] = ObjectId(deal["_id"])
        if deal.get("category_id"):
            deal["category_id"] = ObjectId(deal["category_id"])

        if deal.get("parent_id"):
            deal["parent_id"] = ObjectId(deal["parent_id"])

        if deal.get("price_min"):
            deal["price_min"] = Decimal128(str(deal["price_min"]))

        if deal.get("price_max"):
            deal["price_max"] = Decimal128(str(deal["price_max"]))

        deal['created_at'] = parse(deal['created_at'])
        deal['modified_at'] = parse(deal['modified_at'])

    deal_collection = db.get_collection("deals")

    await deal_collection.insert_many(deals)
