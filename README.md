# Product Search System

A small Python project providing a product search API and a Streamlit frontend.

Files
- `api.py` — HTTP API endpoints (FastAPI/Flask/other)
- `app.py` — application entry or app instance
- `database.py` — database utilities and connection
- `init_db.py` — database initialization script
- `streamlit.py` — Streamlit UI for searching products
- `requirements.txt` — Python dependencies

Requirements
- Python 3.8+

Setup
1. Create and activate a virtual environment:

   `python -m venv venv`

   On Windows:

   `venv\Scripts\activate`

2. Install dependencies:

   `pip install -r requirements.txt`

3. Initialize the database (if used):

   `python init_db.py`

Running
- Run the API server (adjust module name if your app object is in `api.py` or `app.py`):

  `uvicorn app:app --reload`

  or

  `uvicorn api:app --reload`

- Run the Streamlit UI:

  `streamlit run streamlit.py`

Notes
- Confirm which module exposes the ASGI app object (commonly `app:app` or `api:app`) and update the `uvicorn` command accordingly.
- If the project uses a specific database (SQLite, Postgres, etc.), update `database.py` or environment variables before running `init_db.py`.

License
- Add your project license here (e.g., MIT).

Contact
- For questions, open an issue or contact the maintainer.
