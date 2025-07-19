from fastapi import APIRouter, HTTPException, Depends
from controllers.product_controller import (
    create_new_product,
    list_products,
    delete_product,
    edit_product,
)
from models.product_model import ProductCreate
from middleware.auth import JWTBearer

router = APIRouter()
jwt_bearer = JWTBearer()


@router.post("/products", status_code=201)
async def create_product_endpoint(
    product: ProductCreate,
    # token: str = Depends(jwt_bearer)
):
    return create_new_product(product)


@router.get("/products")
async def get_products_endpoint(
    name: str = None,
    size: str = None,
    limit: int = 10,
    offset: int = 0,
    # token: str = Depends(jwt_bearer),
):
    return list_products(name, size, limit, offset)


@router.delete("/products/{product_id}", status_code=204)
async def delete_product_endpoint(
    product_id: str,
    #   token: str = Depends(jwt_bearer)
):
    return delete_product(product_id)


@router.put("/products/{product_id}", status_code=202)
async def edit_product_endpoint(
    product_id: str,
    product: ProductCreate,
    # token: str = Depends(jwt_bearer)
):
    updated_product = edit_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product
