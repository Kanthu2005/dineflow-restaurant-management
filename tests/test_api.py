import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure project root is on path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.main import app

client = TestClient(app)


def test_home_and_health():
    res_home = client.get("/")
    assert res_home.status_code == 200
    assert "Restaurant Management System" in res_home.json()["message"]

    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"


def test_login_and_token_generation():
    # Valid login
    res = client.post("/api/auth/login", json={
        "email": "admin@dineflow.com",
        "password": "Password123!"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["role"] == "ADMIN"
    assert "password" not in data["user"]

    # Invalid password
    res_bad = client.post("/api/auth/login", json={
        "email": "admin@dineflow.com",
        "password": "WrongPassword!"
    })
    assert res_bad.status_code == 400


def test_unauthenticated_request_blocked():
    res = client.get("/api/users")
    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated"


def test_invalid_token_blocked():
    headers = {"Authorization": "Bearer invalid.token.value"}
    res = client.get("/api/users", headers=headers)
    assert res.status_code == 401


def test_auth_me_endpoint():
    login_res = client.post("/api/auth/login", json={
        "email": "admin@dineflow.com",
        "password": "Password123!"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/auth/me", headers=headers)
    assert res.status_code == 200
    user = res.json()
    assert user["email"] == "admin@dineflow.com"
    assert user["role"] == "ADMIN"
    assert "password" not in user


def test_role_based_access_control():
    # Login as Waiter
    w_login = client.post("/api/auth/login", json={
        "email": "waiter@dineflow.com",
        "password": "Password123!"
    })
    w_token = w_login.json()["access_token"]
    w_headers = {"Authorization": f"Bearer {w_token}"}

    # Waiter blocked from User management (requires ADMIN or MANAGER)
    res_forbidden = client.get("/api/users", headers=w_headers)
    assert res_forbidden.status_code == 403
    assert "Forbidden" in res_forbidden.json()["detail"]

    # Waiter allowed to view tables
    res_tables = client.get("/api/tables", headers=w_headers)
    assert res_tables.status_code == 200

    # Login as Admin
    a_login = client.post("/api/auth/login", json={
        "email": "admin@dineflow.com",
        "password": "Password123!"
    })
    a_token = a_login.json()["access_token"]
    a_headers = {"Authorization": f"Bearer {a_token}"}

    # Admin allowed to access /api/users
    res_users = client.get("/api/users", headers=a_headers)
    assert res_users.status_code == 200
    assert len(res_users.json()) >= 1


def test_order_discount_and_item_methods():
    # Login as Admin
    a_login = client.post("/api/auth/login", json={
        "email": "admin@dineflow.com",
        "password": "Password123!"
    })
    token = a_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    import uuid
    uid = uuid.uuid4().hex[:8]
    phone = f"9{uid[:9]}"

    # 1. Create a customer
    cust_res = client.post("/api/customers", headers=headers, json={
        "name": f"Test Customer {uid}",
        "phone": f"9{int(uuid.uuid4().int % 1000000000):09d}",
        "email": f"customer_{uid}@example.com"
    })
    customer_id = cust_res.json()["id"] if cust_res.status_code == 201 else None

    # 2. Create a category and menu item
    cat_res = client.post("/api/menu/categories", headers=headers, json={
        "name": f"Test Category {uid}"
    })
    cat_id = cat_res.json()["id"]

    item_res = client.post("/api/menu/items", headers=headers, json={
        "category_id": cat_id,
        "name": f"Test Burger {phone}",
        "price": 15.50,
        "preparation_time": 15,
        "is_available": True
    })
    assert item_res.status_code == 201
    item_id = item_res.json()["id"]

    # 3. Create an order
    order_res = client.post("/api/orders", headers=headers, json={
        "order_type": "DINE_IN",
        "customer_id": customer_id,
        "created_by": a_login.json()["user"]["id"]
    })
    assert order_res.status_code == 201
    order_id = order_res.json()["id"]

    # 4. Add order item (verifying Decimal128 multiplication bug fix)
    add_res = client.post(f"/api/orders/{order_id}/items", headers=headers, json={
        "menu_item_id": item_id,
        "quantity": 2,
        "special_instructions": "Extra sauce"
    })
    assert add_res.status_code == 201
    order_item_id = add_res.json()["id"]
    assert float(add_res.json()["item_total"]) == 31.0

    # 5. Update order item (verifying update_item implementation)
    up_item_res = client.put(f"/api/orders/{order_id}/items/{order_item_id}", headers=headers, json={
        "quantity": 3,
        "special_instructions": "No onions"
    })
    assert up_item_res.status_code == 200
    assert float(up_item_res.json()["item_total"]) == 46.50

    # 6. Update order discount (verifying update_discount implementation)
    disc_res = client.patch(f"/api/orders/{order_id}/discount", headers=headers, json={
        "discount_amount": 5.0
    })
    assert disc_res.status_code == 200
    assert float(disc_res.json()["discount_amount"]) == 5.0

    # 7. Delete order item (verifying delete_item implementation)
    del_res = client.delete(f"/api/orders/{order_id}/items/{order_item_id}", headers=headers)
    assert del_res.status_code == 200
    assert del_res.json()["message"] == "Order item deleted successfully"


def test_table_and_reservation_flow():
    import uuid
    uid = uuid.uuid4().hex[:6]

    a_login = client.post("/api/auth/login", json={
        "email": "admin@dineflow.com",
        "password": "Password123!"
    })
    headers = {"Authorization": f"Bearer {a_login.json()['access_token']}"}

    # 1. Create table
    table_res = client.post("/api/tables", headers=headers, json={
        "table_number": f"T-{uid}",
        "capacity": 4,
        "location": "PATIO"
    })
    assert table_res.status_code == 201
    table_id = table_res.json()["id"]

    # 2. Get available tables
    avail_res = client.get("/api/tables/available", headers=headers)
    assert avail_res.status_code == 200
    assert any(t["id"] == table_id for t in avail_res.json())

    # 3. Create customer for reservation
    cust_res = client.post("/api/customers", headers=headers, json={
        "name": f"Res Customer {uid}",
        "phone": f"8{int(uuid.uuid4().int % 1000000000):09d}",
        "email": f"res_{uid}@example.com"
    })
    cust_id = cust_res.json()["id"]

    # 4. Create reservation
    res_res = client.post("/api/reservations", headers=headers, json={
        "customer_id": cust_id,
        "table_id": table_id,
        "reservation_date": "2026-10-01",
        "start_time": "19:00:00",
        "end_time": "21:00:00",
        "guest_count": 2,
        "contact_number": "1234567890"
    })
    assert res_res.status_code == 201
    res_id = res_res.json()["id"]

    # 5. Get reservation by customer & table
    by_cust = client.get(f"/api/reservations/customer/{cust_id}", headers=headers)
    assert by_cust.status_code == 200
    assert len(by_cust.json()) >= 1

    by_tbl = client.get(f"/api/reservations/table/{table_id}", headers=headers)
    assert by_tbl.status_code == 200
    assert len(by_tbl.json()) >= 1


def test_ingredient_and_inventory_flow():
    import uuid
    uid = uuid.uuid4().hex[:6]

    a_login = client.post("/api/auth/login", json={
        "email": "admin@dineflow.com",
        "password": "Password123!"
    })
    headers = {"Authorization": f"Bearer {a_login.json()['access_token']}"}

    # 1. Create ingredient
    ing_res = client.post("/api/ingredients", headers=headers, json={
        "name": f"Cheese {uid}",
        "unit": "KG",
        "available_quantity": 20.0,
        "minimum_stock_level": 5.0,
        "cost_per_unit": 8.50
    })
    assert ing_res.status_code == 201
    ing_id = ing_res.json()["id"]

    # 2. Stock movement / update
    stock_res = client.post(f"/api/ingredients/{ing_id}/stock", headers=headers, json={
        "quantity": 5.0
    })
    assert stock_res.status_code == 200
    assert float(stock_res.json()["available_quantity"]) == 25.0

    # 3. Stock status
    status_res = client.get(f"/api/ingredients/{ing_id}/stock-status", headers=headers)
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "NORMAL"


def test_billing_payment_and_refund_flow():
    import uuid
    uid = uuid.uuid4().hex[:6]

    a_login = client.post("/api/auth/login", json={
        "email": "admin@dineflow.com",
        "password": "Password123!"
    })
    user_id = a_login.json()["user"]["id"]
    headers = {"Authorization": f"Bearer {a_login.json()['access_token']}"}

    # 1. Create category & item
    cat_res = client.post("/api/menu/categories", headers=headers, json={
        "name": f"Billing Category {uid}"
    })
    cat_id = cat_res.json()["id"]

    item_res = client.post("/api/menu/items", headers=headers, json={
        "category_id": cat_id,
        "name": f"Billing Steak {uid}",
        "price": 25.0,
        "preparation_time": 20,
        "is_available": True
    })
    item_id = item_res.json()["id"]

    # 2. Create order & add 2 items (subtotal=50.0, tax=2.5, total=52.5)
    order_res = client.post("/api/orders", headers=headers, json={
        "order_type": "TAKEAWAY",
        "created_by": user_id
    })
    order_id = order_res.json()["id"]

    client.post(f"/api/orders/{order_id}/items", headers=headers, json={
        "menu_item_id": item_id,
        "quantity": 2
    })

    # 3. Create invoice for order
    inv_res = client.post("/api/invoices", headers=headers, json={
        "order_id": order_id
    })
    assert inv_res.status_code == 201
    inv_id = inv_res.json()["id"]
    assert float(inv_res.json()["total_amount"]) == 52.5

    # 4. Get invoice by order
    inv_check = client.get(f"/api/invoices/order/{order_id}", headers=headers)
    assert inv_check.status_code == 200
    assert inv_check.json()["id"] == inv_id

    # 5. Create payment
    pay_res = client.post("/api/payments", headers=headers, json={
        "invoice_id": inv_id,
        "amount": 52.5,
        "payment_method": "CASH",
        "recorded_by": user_id
    })
    assert pay_res.status_code == 201
    pay_id = pay_res.json()["id"]

    # 6. Create refund
    ref_res = client.post("/api/refunds", headers=headers, json={
        "payment_id": pay_id,
        "order_id": order_id,
        "requested_amount": 10.0,
        "reason": "Item canceled"
    })
    assert ref_res.status_code == 201
    ref_id = ref_res.json()["id"]

    # 7. Approve refund
    appr_res = client.patch(f"/api/refunds/{ref_id}/approve", headers=headers, json={
        "approved_amount": 10.0,
        "approved_by": user_id
    })
    assert appr_res.status_code == 200
    assert appr_res.json()["status"] == "APPROVED"


def test_customer_feedback_flow():
    import uuid
    uid = uuid.uuid4().hex[:6]

    a_login = client.post("/api/auth/login", json={
        "email": "admin@dineflow.com",
        "password": "Password123!"
    })
    headers = {"Authorization": f"Bearer {a_login.json()['access_token']}"}
    user_id = a_login.json()["user"]["id"]

    # 1. Create customer and order
    cust_res = client.post("/api/customers", headers=headers, json={
        "name": f"Feedback Customer {uid}",
        "phone": f"7{int(uuid.uuid4().int % 1000000000):09d}",
        "email": f"fb_{uid}@example.com"
    })
    cust_id = cust_res.json()["id"]

    order_res = client.post("/api/orders", headers=headers, json={
        "order_type": "DINE_IN",
        "customer_id": cust_id,
        "created_by": user_id
    })
    order_id = order_res.json()["id"]

    # 2. Create feedback for the order
    fb_res = client.post(f"/api/orders/{order_id}/feedback", headers=headers, json={
        "customer_id": cust_id,
        "rating": 5,
        "food_rating": 5,
        "service_rating": 4,
        "comments": "Excellent food and service!"
    })
    assert fb_res.status_code == 201
    fb_id = fb_res.json()["id"]

    # 3. Get feedback summary
    summary_res = client.get("/api/feedback/summary", headers=headers)
    assert summary_res.status_code == 200
    assert "average_rating" in summary_res.json()


