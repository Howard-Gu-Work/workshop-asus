from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_products(client: TestClient) -> None:
    response = client.get("/products")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 6
    assert body["page"] == 1
    assert body["page_size"] == 20
    assert body["items"][0]["name"] == "Zenbook 14 OLED"


def test_list_products_supports_case_insensitive_search(client: TestClient) -> None:
    response = client.get("/products", params={"q": "proart"})

    assert response.status_code == 200
    assert response.json()["items"] == [
        {
            "id": 3,
            "name": "ProArt P16",
            "category": "Creator Laptop",
            "price": 79900.0,
        },
        {
            "id": 6,
            "name": "ProArt Display PA279CRV",
            "category": "Monitor",
            "price": 15900.0,
        },
    ]


def test_list_products_can_combine_query_parameters(client: TestClient) -> None:
    response = client.get(
        "/products",
        params={
            "q": "gaming",
            "sort": "price",
            "order": "asc",
            "page": 1,
            "page_size": 2,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": 4,
                "name": "TUF Gaming A15",
                "category": "Gaming Laptop",
                "price": 38900.0,
            },
            {
                "id": 2,
                "name": "ROG Zephyrus G14",
                "category": "Gaming Laptop",
                "price": 62900.0,
            },
        ],
        "total": 2,
        "page": 1,
        "page_size": 2,
    }


def test_list_products_rejects_invalid_query_parameters(client: TestClient) -> None:
    response = client.get("/products", params={"page_size": 21})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "page_size"]
    assert response.json()["detail"][0]["type"] == "less_than_equal"


def test_get_product(client: TestClient) -> None:
    response = client.get("/products/2")

    assert response.status_code == 200
    assert response.json()["name"] == "ROG Zephyrus G14"


def test_get_missing_product(client: TestClient) -> None:
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
