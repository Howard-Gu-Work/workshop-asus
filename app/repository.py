from typing import Literal

from app.models import Product

SortField = Literal["id", "name", "category", "price"]
SortOrder = Literal["asc", "desc"]

PRODUCTS = [
    Product(id=1, name="Zenbook 14 OLED", category="Laptop", price=42900),
    Product(id=2, name="ROG Zephyrus G14", category="Gaming Laptop", price=62900),
    Product(id=3, name="ProArt P16", category="Creator Laptop", price=79900),
    Product(id=4, name="TUF Gaming A15", category="Gaming Laptop", price=38900),
    Product(id=5, name="ROG Ally X", category="Handheld", price=26900),
    Product(id=6, name="ProArt Display PA279CRV", category="Monitor", price=15900),
]


def list_products(
    *,
    q: str | None = None,
    sort: SortField = "id",
    order: SortOrder = "asc",
) -> list[Product]:
    products = PRODUCTS.copy()
    if q is not None:
        query = q.casefold()
        products = [
            product
            for product in products
            if query in product.name.casefold() or query in product.category.casefold()
        ]

    reverse = order == "desc"
    if sort == "name":
        return sorted(products, key=lambda product: product.name.casefold(), reverse=reverse)
    if sort == "category":
        return sorted(products, key=lambda product: product.category.casefold(), reverse=reverse)
    if sort == "price":
        return sorted(products, key=lambda product: product.price, reverse=reverse)
    return sorted(products, key=lambda product: product.id, reverse=reverse)


def get_product(product_id: int) -> Product | None:
    return next((product for product in PRODUCTS if product.id == product_id), None)
