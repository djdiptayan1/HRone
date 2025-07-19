from fastapi import APIRouter, HTTPException, Depends
from controllers.order_controller import (
    create_new_order,
    get_user_orders,
    delete_order,
    edit_order,
)
from models.order_model import OrderCreate
from middleware.auth import JWTBearer

router = APIRouter()
jwt_bearer = JWTBearer()


@router.post("/orders", status_code=201)
async def create_order_endpoint(
    order: OrderCreate,
    # token: str = Depends(jwt_bearer)
):
    return create_new_order(order)


@router.get("/orders/{user_id}")
async def get_orders_endpoint(
    user_id: str,
    limit: int = 6,
    offset: int = 0,
    # token: str = Depends(jwt_bearer)
):
    return get_user_orders(user_id, limit, offset)


@router.delete("/orders/{order_id}", status_code=204)
async def delete_order_endpoint(
    order_id: str,
    # token: str = Depends(jwt_bearer)
):
    result = delete_order(order_id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted successfully"}


@router.put("/orders/{order_id}", status_code=202)
async def edit_order_endpoint(
    order_id: str,
    order: OrderCreate,
    # token: str = Depends(jwt_bearer)
):
    result = edit_order(order_id, order)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return {"detail": "Order updated successfully"}
