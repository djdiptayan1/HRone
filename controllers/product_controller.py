from db.product_repository import create_product
from models.product_model import ProductCreate, ProductResponse

from db.database import get_db
from bson import ObjectId
import re


def get_products(
    name: str = None,
    size: str = None,
    product_ids: list = None,
    limit: int = 10,
    offset: int = 0,
):
    db = get_db()
    query = {}

    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}

    if size:
        query["sizes.size"] = size

    if product_ids:
        object_ids = [ObjectId(pid) for pid in product_ids]
        query["_id"] = {"$in": object_ids}

    products = db.products.find(query).skip(offset).limit(limit)
    return [
        {"id": str(product["_id"]), "name": product["name"], "price": product["price"]}
        for product in products
    ], db.products.count_documents(query)


def create_new_product(product: ProductCreate):
    # product_id = create_product(product)
    db = get_db()
    product = product.dict()
    result = db.products.insert_one(product)

    return {"id": str(result.inserted_id)}


def list_products(name: str = None, size: str = None, limit: int = 10, offset: int = 0):
    products_list, total = get_products(name, size, None, limit, offset)

    next_offset = offset + limit if offset + limit < total else None
    prev_offset = offset - limit if offset - limit >= 0 else None

    return {
        "data": products_list,
        "page": {
            "next": str(next_offset) if next_offset else None,
            "limit": limit,
            "previous": str(prev_offset) if prev_offset else None,
        },
    }

def delete_product(product_id: str):
    db = get_db()
    result = db.products.delete_one({"_id": ObjectId(product_id)})
    return {"deleted": result.deleted_count > 0}

def edit_product(product_id: str, product: ProductCreate):
    db = get_db()
    product_data = product.dict()
    result = db.products.update_one(
        {"_id": ObjectId(product_id)}, {"$set": product_data}
    )
    
    if result.matched_count == 0:
        return {"error": "Product not found"}
    
    return {"id": product_id, "name": product_data["name"], "price": product_data["price"]}