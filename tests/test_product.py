
from fastapi.testclient import TestClient

from run import app

client = TestClient(app)

def test_read_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_get_product():
    # Create a product
    product_data = {"name": "Test Product", "description": "A test", "price": 9.99}
    create_resp = client.post("/products", json=product_data)
    assert create_resp.status_code == 200
    created = create_resp.json()
    assert created["name"] == product_data["name"]
    assert created["description"] == product_data["description"]
    assert created["price"] == product_data["price"]
    product_id = created["id"]

    # Get the product
    get_resp = client.get(f"/products/{product_id}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["id"] == product_id
    assert fetched["name"] == product_data["name"]

    # Update the product
    update_data = {"name": "Updated Product", "description": "Updated desc", "price": 19.99}
    update_resp = client.put(f"/products/{product_id}", json=update_data)
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["name"] == update_data["name"]
    assert updated["price"] == update_data["price"]

    # Delete the product
    delete_resp = client.delete(f"/products/{product_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["detail"] == "Product deleted"

    # Ensure product is gone
    get_resp = client.get(f"/products/{product_id}")
    assert get_resp.status_code == 404
