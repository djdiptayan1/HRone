from fastapi import FastAPI
import uvicorn
from routes.product_routes import router as product_router
from routes.order_routes import router as order_router
from routes.auth_routes import router as auth_router

app = FastAPI(
    title="E-commerce API",
    description="A comprehensive e-commerce API",
    version="1.0.0",
)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])

app.include_router(product_router, prefix="/api/v1", tags=["Products"])
app.include_router(order_router, prefix="/api/v1", tags=["Orders"])


@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "E-commerce API Service",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
