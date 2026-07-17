from collections.abc import Callable
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

SORT_KEYS: dict[SortField, Callable[[Product], int | float | str]] = {
    "id": lambda product: product.id,
    "name": lambda product: product.name.casefold(),
    "category": lambda product: product.category.casefold(),
    "price": lambda product: product.price,
}


def list_products(
    *,
    q: str | None = None,
    sort: SortField = "id",
    order: SortOrder = "asc",
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Product], int]:
    products = PRODUCTS.copy()
    if q is not None:
        query = q.casefold()
        products = [
            product
            for product in products
            if _matches_query(product, query)
        ]

    reverse = order == "desc"
    products = sorted(products, key=SORT_KEYS[sort], reverse=reverse)
    total = len(products)
    start = (page - 1) * page_size
    end = start + page_size
    return products[start:end], total


def get_product(product_id: int) -> Product | None:
    return next((product for product in PRODUCTS if product.id == product_id), None)


def _matches_query(product: Product, query: str) -> bool:
    name = product.name.casefold()
    category = product.category.casefold()
    return query in name or query in category
