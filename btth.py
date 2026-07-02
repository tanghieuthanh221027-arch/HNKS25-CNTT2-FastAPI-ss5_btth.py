from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products = [
    {"id": 1, "name": "Keyboard", "price": 500000},
    {"id": 2, "name": "Mouse", "price": 300000}
]

class ProductRequest(BaseModel):
    name: str
    price: float

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(request: ProductRequest):
    if request.name.strip() == "":
        raise HTTPException(
            status_code=400, 
            detail="Product name cannot be empty"
        )
    
    if request.price <= 0:
        raise HTTPException(
            status_code=400, 
            detail="Price must be greater than 0"
        )
    
    new_product = {
        "id": len(products) + 1,
        "name": request.name,
        "price": request.price
    }
    
    products.append(new_product)
    return {
        "message": "Product created successfully",
        "data": new_product
    }

@app.get("/products")
def get_products():
    return {
        "data": products
    }

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {
                "message": "Product deleted successfully"
            }
    raise HTTPException(status_code=404, detail="Product not found")