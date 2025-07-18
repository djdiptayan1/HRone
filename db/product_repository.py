from db.database import get_db
from bson import ObjectId
import re


def create_product(product_data):
    db = get_db()
    product = product_data.dict()
    result = db.products.insert_one(product)
    return str(result.inserted_id)


def get_products(name: str = None, size: str = None, limit: int = 10, offset: int = 0):
    db = get_db()
    query = {}

    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}

    if size:
        query["sizes.size"] = size

    products = db.products.find(query).skip(offset).limit(limit)
    return [
        {"id": str(product["_id"]), "name": product["name"], "price": product["price"]}
        for product in products
    ], db.products.count_documents(query)
