from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection

app = FastAPI(
    title="Product Search API",
    description="API for searching and managing products",
    version="1.0.0"
)


class ProductCreate(BaseModel):
    name: str


@app.get("/products")
def get_products():
    """Fetch all products."""

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name FROM products"
        )

        products = cursor.fetchall()

    if not products:
        raise HTTPException(
            status_code=404,
            detail=f"No products found matching '{name}'."
        )

    return [
        {
            "id": product[0],
            "name": product[1]
        }
        for product in products
    ]


@app.post("/products", status_code=201)
def create_product(item: ProductCreate):
    normalized = item.name.strip()
    if not normalized:
        raise HTTPException(
            status_code=400,
            detail="Product name cannot be empty."
        )

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name) VALUES (?)",
            (normalized,)
        )
        conn.commit()
        product_id = cursor.lastrowid

    return {"id": product_id, "name": normalized}


@app.get("/search")
def search_products(name: str):
    """Search products by name."""

    if not name.strip():
        raise HTTPException(
            status_code=400,
            detail="Search term cannot be empty."
        )

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name
            FROM products
            WHERE LOWER(name) LIKE LOWER(?)
            """,
            (f"%{name}%",)
        )

        products = cursor.fetchall()

    return [
        {
            "id": product[0],
            "name": product[1]
        }
        for product in products
    ]