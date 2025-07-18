# E-commerce Backend API

A e-commerce backend application built with **FastAPI** and **MongoDB**, featuring product management, order processing, and inventory control.

## 🚀 Features

- **Product Management**: Create and list products with size variants
- **Order Processing**: Place orders with real-time inventory validation
- **Inventory Management**: Automatic stock deduction and overselling prevention
- **Pagination**: Efficient data retrieval with offset-based pagination
- **Search & Filtering**: Advanced product search by name and size
- **Database Transactions**: ACID compliance for order processing
- **Environment Configuration**: Secure credential management with .env

## 🛠 Tech Stack

- **Backend Framework**: FastAPI (Python 3.11)
- **Database**: MongoDB with PyMongo
- **Validation**: Pydantic Models
- **Environment**: python-dotenv
- **Server**: Uvicorn ASGI Server

## 📁 Project Structure

```
HRone/
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── readme.md             # Project documentation
├── controllers/          # Business logic layer
│   ├── product_controller.py
│   └── order_controller.py
├── db/                   # Database layer
│   ├── database.py       # MongoDB connection
│   ├── product_repository.py
│   └── order_repository.py
├── models/               # Pydantic data models
│   ├── product_model.py
│   └── order_model.py
└── routes/               # API route definitions
    ├── product_routes.py
    └── order_routes.py
```

## 🔧 Setup & Installation

### Prerequisites
- Python 3.10 or higher
- MongoDB Atlas account (or local MongoDB)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/djdiptayan1/HRone.git
cd HRone
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=ecommerce_db
```

### 5. Run the Application
```bash
python app.py
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Interactive API Docs
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🛍 API Endpoints

### Products

#### Create Product
```http
POST /api/v1/products
```

**Request Body:**
```json
{
    "name": "T-Shirt",
    "price": 25.99,
    "sizes": [
        {"size": "S", "quantity": 10},
        {"size": "M", "quantity": 15},
        {"size": "L", "quantity": 8}
    ]
}
```

**Response:**
```json
{
    "id": "507f1f77bcf86cd799439011"
}
```
**Status Code:** `201 Created`

#### List Products
```http
GET /api/v1/products?name=shirt&size=M&limit=10&offset=0
```

**Query Parameters:**
- `name` (optional): Search by product name (supports partial matching)
- `size` (optional): Filter by available size
- `limit` (optional): Number of products to return (default: 10)
- `offset` (optional): Number of products to skip (default: 0)

**Response:**
```json
{
    "data": [
        {
            "id": "507f1f77bcf86cd799439011",
            "name": "T-Shirt",
            "price": 25.99
        }
    ],
    "page": {
        "next": "10",
        "limit": 10,
        "previous": null
    }
}
```
**Status Code:** `200 OK`

#### Update Product
```http
PUT /api/v1/products/{product_id}
```

**Request Body:**
```json
{
    "name": "Updated T-Shirt",
    "price": 29.99,
    "sizes": [
        {"size": "S", "quantity": 5},
        {"size": "M", "quantity": 10},
        {"size": "L", "quantity": 15}
    ]
}
```

**Response:**
```json
{
    "message": "Product updated successfully"
}
```
**Status Code:** `202 Accepted`

#### Delete Product
```http
DELETE /api/v1/products/{product_id}
```

**Response:**
```json
{
    "message": "Product deleted successfully"
}
```
**Status Code:** `204 No Content`

### Orders

#### Create Order
```http
POST /api/v1/orders
```

**Request Body:**
```json
{
    "userId": "user_123",
    "items": [
        {
            "productId": "507f1f77bcf86cd799439011",
            "qty": 2
        }
    ]
}
```

**Response:**
```json
{
    "id": "507f1f77bcf86cd799439012"
}
```
**Status Code:** `201 Created`

#### Get User Orders
```http
GET /api/v1/orders/{user_id}?limit=10&offset=0
```

**Response:**
```json
{
    "data": [
        {
            "id": "507f1f77bcf86cd799439012",
            "items": [
                {
                    "productDetails": {
                        "id": "507f1f77bcf86cd799439011",
                        "name": "T-Shirt"
                    },
                    "qty": 2
                }
            ],
            "total": 51.98
        }
    ],
    "page": {
        "next": "10",
        "limit": 10,
        "previous": null
    }
}
```
**Status Code:** `200 OK`

#### Update Order
```http
PUT /api/v1/orders/{order_id}
```

**Request Body:**
```json
{
    "userId": "user_123",
    "items": [
        {
            "productId": "507f1f77bcf86cd799439011",
            "qty": 3
        }
    ]
}
```

**Response:**
```json
{
    "message": "Order updated successfully"
}
```
**Status Code:** `202 Accepted`

#### Cancel Order
```http
DELETE /api/v1/orders/{order_id}
```

**Response:**
```json
{
    "message": "Order cancelled successfully"
}
```
**Status Code:** `204 No Content`

## 🔒 Security Features

- **Environment Variables**: Sensitive data stored in .env files
- **Input Validation**: Pydantic models ensure data integrity
- **Error Handling**: Comprehensive error responses
- **Database Transactions**: Atomic operations prevent data corruption

## 📊 Database Schema

### Products Collection
```json
{
    "_id": "ObjectId",
    "name": "string",
    "price": "number",
    "sizes": [
        {
            "size": "string",
            "quantity": "number"
        }
    ]
}
```

### Orders Collection
```json
{
    "_id": "ObjectId",
    "userId": "string",
    "items": [
        {
            "productId": "string",
            "qty": "number"
        }
    ]
}
```

## 🎯 Key Features

### Inventory Management
- **Real-time Stock Validation**: Prevents overselling
- **Automatic Deduction**: Stock levels update on successful orders
- **Size-based Inventory**: Tracks quantities per product size
- **FIFO Logic**: Deducts from available sizes in order

### Performance Optimizations
- **Batch Product Fetching**: Single query for multiple products
- **Efficient Pagination**: Offset-based navigation
- **Index Support**: Optimized database queries

### Error Handling
- **Product Not Found**: Clear error messages
- **Insufficient Stock**: Detailed availability information
- **Validation Errors**: Pydantic model validation

## 🧪 Testing

### Manual Testing with curl

**Create a Product:**
```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jeans",
    "price": 59.99,
    "sizes": [{"size": "32", "quantity": 5}]
  }'
```

**Place an Order:**
```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user_123",
    "items": [{"productId": "PRODUCT_ID_HERE", "qty": 1}]
  }'
```

**Update a Product:**
```bash
curl -X PUT "http://localhost:8000/api/v1/products/PRODUCT_ID_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Jeans",
    "price": 69.99,
    "sizes": [{"size": "32", "quantity": 8}]
  }'
```

**Delete a Product:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/products/PRODUCT_ID_HERE"
```

**Update an Order:**
```bash
curl -X PUT "http://localhost:8000/api/v1/orders/ORDER_ID_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user_123",
    "items": [{"productId": "PRODUCT_ID_HERE", "qty": 2}]
  }'
```

**Cancel an Order:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/orders/ORDER_ID_HERE"
```

## 📝 Development Notes

### Architecture Patterns
- **Repository Pattern**: Separation of data access logic
- **Controller Pattern**: Business logic encapsulation
- **Model-View-Controller**: Clear separation of concerns

### Code Organization
- **models/**: Pydantic schemas for request/response validation
- **controllers/**: Business logic and data processing
- **routes/**: FastAPI route definitions and HTTP handling
- **db/**: Database connection and repository implementations

## 🚀 Quick Start Commands

```bash
# Clone and setup
git clone https://github.com/djdiptayan1/HRone.git
cd HRone
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
echo "MONGO_URI=your_mongodb_uri" > .env
echo "DB_NAME=ecommerce_db" >> .env

# Run the application
python app.py
```