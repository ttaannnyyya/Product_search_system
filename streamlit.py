import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Product Search System",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Product Search System")

# ----------------------------
# Add Product Section
# ----------------------------

st.subheader("Add Product")

new_product = st.text_input(
    "Enter product name",
    key="add_product"
)

if st.button("Add Product"):

    if not new_product.strip():
        st.warning("Please enter a product name.")
    else:
        response = requests.post(
            f"{API_BASE_URL}/products",
            json={"name": new_product}
        )

        if response.status_code == 201:
            st.success("Product added successfully.")
        else:
            st.error("Failed to add product.")

st.divider()

# ----------------------------
# Search Product Section
# ----------------------------

st.subheader("Search Products")

search_term = st.text_input(
    "Search by product name",
    key="search_product"
)

if st.button("Search"):

    if not search_term.strip():
        st.warning("Please enter a search term.")
    else:

        response = requests.get(
            f"{API_BASE_URL}/search",
            params={"name": search_term}
        )

        if response.status_code == 200:

            products = response.json()

            if products:

                st.success(
                    f"{len(products)} product(s) found."
                )

                for product in products:
                    st.write(
                        f"• {product['name']}"
                    )

            else:
                st.info(
                    "No products found."
                )

        else:
            st.error(
                "Something went wrong."
            )

st.divider()

# ----------------------------
# View All Products
# ----------------------------

if st.button("View All Products"):

    response = requests.get(
        f"{API_BASE_URL}/products"
    )

    if response.status_code == 200:

        products = response.json()

        st.subheader("Available Products")

        for product in products:
            st.write(
                f"• {product['name']}"
            )