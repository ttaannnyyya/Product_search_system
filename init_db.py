from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

products = [
    ("iPhone 15",),
    ("Samsung Galaxy S24",),
    ("MacBook Air",),
    ("AirPods Pro",)
]

cursor.executemany(
    "INSERT INTO products (name) VALUES (?)",
    products
)

conn.commit()
conn.close()

print("Database initialized successfully.")