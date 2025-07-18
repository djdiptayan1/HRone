from fastapi import FastAPI
import uvicorn
from routes.product_routes import router as product_router
from routes.order_routes import router as order_router

app = FastAPI()

app.include_router(product_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Ecommerce API Service"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
