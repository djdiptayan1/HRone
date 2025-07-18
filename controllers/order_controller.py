from db.order_repository import create_order, get_orders
from controllers.product_controller import get_products
from models.order_model import OrderCreate, OrderResponse, OrderItemResponse
from models.product_model import OrderProductResponse
from db.database import get_db
from bson import ObjectId


def create_new_order(order: OrderCreate):
    db = get_db()
    for item in order.items:
        product = db.products.find_one({"_id": ObjectId(item.productId)})
        if not product:
            return {"error": f"Product with ID {item.productId} not found"}

        total_available = 0
        if "sizes" in product and isinstance(product["sizes"], list):
            for size_obj in product["sizes"]:
                total_available += size_obj.get("quantity", 0)
        else:
            total_available = product.get("quantity", 0)

        if total_available < item.qty:
            return {
                "error": f"Insufficient stock for {product['name']}. Available: {total_available}, Requested: {item.qty}"
            }

    try:
        with db.client.start_session() as session:
            with session.start_transaction():
                order_dict = order.dict()
                result = db.orders.insert_one(order_dict, session=session)

                for item in order.items:
                    remaining_qty = item.qty
                    product = db.products.find_one(
                        {"_id": ObjectId(item.productId)}, session=session
                    )

                    for i, size_obj in enumerate(product["sizes"]):
                        if remaining_qty <= 0:
                            break

                        available = size_obj["quantity"]
                        to_deduct = min(available, remaining_qty)

                        if to_deduct > 0:
                            db.products.update_one(
                                {"_id": ObjectId(item.productId)},
                                {"$inc": {f"sizes.{i}.quantity": -to_deduct}},
                                session=session,
                            )
                            remaining_qty -= to_deduct

                return {"id": str(result.inserted_id)}

    except Exception as e:
        return {"error": f"Failed to create order: {str(e)}"}


def get_user_orders(user_id: str, limit: int = 10, offset: int = 0):
    orders, total = get_orders(user_id, limit, offset)

    all_product_ids = []
    for order in orders:
        for item in order["items"]:
            if item["productId"] not in all_product_ids:
                all_product_ids.append(item["productId"])

    products_list, _ = get_products(product_ids=all_product_ids)
    products_dict = {product["id"]: product for product in products_list}

    response_orders = []

    for order in orders:
        order_items = []
        total_price = 0

        for item in order["items"]:
            product = products_dict.get(item["productId"])
            if product:
                product_details = OrderProductResponse(
                    id=product["id"], name=product["name"]
                )
                item_total = product["price"] * item["qty"]
                total_price += item_total

                order_items.append(
                    OrderItemResponse(
                        productDetails=product_details,
                        qty=item["qty"],
                    )
                )

        response_orders.append(
            OrderResponse(
                id=str(order["_id"]),
                items=order_items,
                total=total_price,
            )
        )

    next_offset = offset + limit if offset + limit < total else None
    prev_offset = offset - limit if offset - limit >= 0 else None

    return {
        "data": response_orders,
        "page": {
            "next": str(next_offset) if next_offset else None,
            "limit": limit,
            "previous": str(prev_offset) if prev_offset else None,
        },
    }


def delete_order(order_id: str):
    db = get_db()
    result = db.orders.delete_one({"_id": ObjectId(order_id)})

    if result.deleted_count == 0:
        return {"error": "Order not found"}

    return {"message": "Order deleted successfully"}


def edit_order(order_id: str, order: OrderCreate):
    db = get_db()
    order_dict = order.dict()
    result = db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": order_dict})

    if result.matched_count == 0:
        return {"error": "Order not found"}

    return {"message": "Order updated successfully"}
