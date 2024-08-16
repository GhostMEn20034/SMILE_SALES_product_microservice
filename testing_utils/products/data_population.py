import json
from pathlib import Path

from bson import ObjectId, Decimal128
from dateutil.parser import parse
from motor.motor_asyncio import AsyncIOMotorDatabase

root_path = Path(__file__).parent.parent.parent

async def populate_product_data(db: AsyncIOMotorDatabase):
    with open(root_path / 'test_data/test_data_products.json', 'r') as f:
        products = json.load(f)

    for product in products:
        product["_id"] = ObjectId(product["_id"])
        product["price"] = Decimal128(str(product["price"]))
        product["tax_rate"] = Decimal128(str(product["tax_rate"]))
        product["discount_rate"] = Decimal128(str(product["discount_rate"])) if product["discount_rate"] else None

        product["parent_id"] = ObjectId(product["parent_id"]) if product["parent_id"] else None
        product["category"] = ObjectId(product["category"])

        product['created_at'] = parse(product['created_at'])
        product['modified_at'] = parse(product['modified_at'])

    product_collection = db.get_collection("products")

    await product_collection.insert_many(products)
