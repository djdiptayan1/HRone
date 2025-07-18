from db.database import get_db
from bson import ObjectId


def create_order(order_data):
    db = get_db()
    order = order_data.dict()
    result = db.orders.insert_one(order)
    return str(result.inserted_id)


def get_orders(user_id: str, limit: int = 10, offset: int = 0):
    db = get_db()
    query = {"userId": user_id}

    orders = db.orders.find(query).skip(offset).limit(limit)
    return list(orders), db.orders.count_documents(query)
