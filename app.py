from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
import sqlite3
from database import get_connection

app = FastAPI(
    title="Product Search API",
    description="API for searching and managing products",
    version="1.0.0"
)


class ProductCreate(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=100)


@app.get("/products")
def get_products():
    """Fetch all products."""

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM products")
        products = cursor.fetchall()

    if not products:
        raise HTTPException(
            status_code=404,
            detail="No products found."
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

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM products WHERE LOWER(name) = LOWER(?)",
            (normalized,)
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="Product already exists."
            )

        try:
            cursor.execute(
                "INSERT INTO products (name) VALUES (?)",
                (normalized,)
            )
            conn.commit()
            product_id = cursor.lastrowid
        except sqlite3.Error as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {exc}"
            )

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