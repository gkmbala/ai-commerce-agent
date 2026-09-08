import json
from pathlib import Path

from .database import get_connection


PRODUCT_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "products.json"
)


def load_products():
    with open(PRODUCT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_products(
    query="",
    max_price=None,
    category=None,
    use_case=None
):
    products = load_products()
    results = []

    for product in products:

        searchable_text = (
            product["name"]
            + " "
            + product["brand"]
            + " "
            + product["category"]
            + " "
            + product["description"]
            + " "
            + " ".join(product.get("use_cases", []))
        ).lower()

        if query and query.lower() not in searchable_text:
            continue

        if max_price is not None:
            if product["price"] > max_price:
                continue

        if category:
            if product["category"].lower() != category.lower():
                continue

        if use_case:
            use_cases = [
                item.lower()
                for item in product.get("use_cases", [])
            ]

            if use_case.lower() not in use_cases:
                continue

        results.append(product)

    return results


def check_inventory(product_id: int):

    products = load_products()

    for product in products:

        if product["id"] == product_id:

            return {
                "product_id": product_id,
                "sku": product["sku"],
                "name": product["name"],
                "stock": product["stock"],
                "available": product["stock"] > 0
            }

    return {
        "product_id": product_id,
        "stock": 0,
        "available": False
    }


def add_to_cart(product_id: int, quantity: int = 1):

    if quantity < 1:
        return {
            "success": False,
            "message": "Quantity must be at least 1."
        }

    inventory = check_inventory(product_id)

    if not inventory["available"]:

        return {
            "success": False,
            "message": "Product is out of stock."
        }

    if quantity > inventory["stock"]:

        return {
            "success": False,
            "message": (
                f"Only {inventory['stock']} unit(s) "
                "are available."
            )
        }

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO carts(product_id, quantity)
        VALUES (?, ?)
        """,
        (product_id, quantity)
    )

    connection.commit()
    connection.close()

    return {
        "success": True,
        "product_id": product_id,
        "quantity": quantity,
        "message": "Product added to cart."
    }


def get_cart():

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT product_id, quantity
        FROM carts
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    products = {
        product["id"]: product
        for product in load_products()
    }

    cart = []

    for row in rows:

        product = products.get(row["product_id"])

        if product:

            cart.append(
                {
                    "product_id": product["id"],
                    "sku": product["sku"],
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": row["quantity"]
                }
            )

    return cart