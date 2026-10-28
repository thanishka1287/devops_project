"""
Automated Pytest test suite for DevOps Bookshelf.
Covers:
- Homepage loading & structure
- Catalog browsing & rendering
- Search & filtering functionality
- Book details viewing & 404 handling
- Shopping cart lifecycle (add, update, increase, decrease, remove, clear)
- Checkout form validation (missing fields, invalid email, empty cart)
- Database persistence for orders and order_items
- Health check monitoring endpoint
- Idempotent database initialization
"""

import json
from db import get_db_connection, init_db


def test_homepage_loads(client):
    """Verify that the homepage loads with status code 200 and displays bookstore title."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "DevOps" in html
    assert "Bookshelf" in html
    assert "Catalog" in html


def test_books_display(client):
    """Verify that sample books seeded in the SQLite database appear on the homepage."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Docker Deep Dive" in html
    assert "The Phoenix Project" in html
    assert "Clean Code" in html


def test_search_books_by_title(client):
    """Verify searching for books by title returns only matching books."""
    response = client.get("/?q=Docker")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Docker Deep Dive" in html
    assert "Clean Code" not in html


def test_search_books_by_author(client):
    """Verify searching for books by author name."""
    response = client.get("/?q=Martin")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    # Robert C. Martin wrote Clean Code, Martin Kleppmann wrote Designing Data-Intensive Applications
    assert "Clean Code" in html or "Designing Data-Intensive Applications" in html
    assert "Fluent Python" not in html


def test_filter_books_by_category(client):
    """Verify category filtering isolates books of the selected category."""
    response = client.get("/?category=Software+Engineering")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Clean Code" in html
    assert "Docker Deep Dive" not in html


def test_empty_search_message(client):
    """Verify that a search yielding no results shows a friendly empty state."""
    response = client.get("/?q=NonExistentGibberish12345")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "No books found" in html


def test_book_details_view_valid(client):
    """Verify viewing details of an existing book by its primary key ID."""
    response = client.get("/books/1")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Docker Deep Dive" in html
    assert "Nigel Poulton" in html
    assert "Add to Shopping Cart" in html


def test_book_details_view_invalid_returns_404(client):
    """Verify that requesting a non-existent book ID returns a 404 error page."""
    response = client.get("/books/99999")
    assert response.status_code == 404
    html = response.get_data(as_text=True)
    assert "404" in html


def test_cart_operations(client):
    """Verify full shopping cart lifecycle: add, update, and clear."""
    # 1. Add 2 copies of book 1
    add_resp = client.post("/cart/add", data={"book_id": 1, "quantity": 2}, follow_redirects=True)
    assert add_resp.status_code == 200
    html = add_resp.get_data(as_text=True)
    assert "Docker Deep Dive" in html
    assert "69.98" in html or "34.99" in html

    # 2. Increase quantity of book 1
    inc_resp = client.post("/cart/update", data={"book_id": "1", "action": "increase"}, follow_redirects=True)
    assert inc_resp.status_code == 200
    html = inc_resp.get_data(as_text=True)
    assert "Updated quantity" in html

    # 3. Decrease quantity of book 1
    dec_resp = client.post("/cart/update", data={"book_id": "1", "action": "decrease"}, follow_redirects=True)
    assert dec_resp.status_code == 200
    html = dec_resp.get_data(as_text=True)
    assert "Updated quantity" in html

    # 4. Remove book 1 from cart
    rem_resp = client.post("/cart/update", data={"book_id": "1", "action": "remove"}, follow_redirects=True)
    assert rem_resp.status_code == 200
    html = rem_resp.get_data(as_text=True)
    assert "Your Cart is Empty" in html


def test_checkout_empty_cart_redirect(client):
    """Verify navigating to checkout with an empty cart redirects back to catalog with warning."""
    response = client.get("/checkout", follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Your cart is empty" in html


def test_checkout_validation_errors(client):
    """Verify checkout form validation prevents empty or invalid inputs."""
    # First add a book to the cart
    client.post("/cart/add", data={"book_id": 1, "quantity": 1})

    # Missing customer name
    resp1 = client.post(
        "/checkout",
        data={"customer_name": "", "customer_email": "student@college.edu", "customer_address": "Campus Hall"},
        follow_redirects=True,
    )
    assert "Full Name is required." in resp1.get_data(as_text=True)

    # Invalid email address format
    resp2 = client.post(
        "/checkout",
        data={"customer_name": "John Doe", "customer_email": "not-an-email", "customer_address": "Campus Hall"},
        follow_redirects=True,
    )
    assert "Please enter a valid email address." in resp2.get_data(as_text=True)

    # Missing address
    resp3 = client.post(
        "/checkout",
        data={"customer_name": "John Doe", "customer_email": "john@college.edu", "customer_address": ""},
        follow_redirects=True,
    )
    assert "Shipping Address is required." in resp3.get_data(as_text=True)


def test_successful_order_placement_and_database_persistence(client, app):
    """
    Verify complete order placement:
    1. Items added to cart
    2. Valid customer details submitted
    3. Order and order_items records created and persisted in SQLite
    4. Confirmation receipt presented with correct data
    5. Shopping cart emptied
    """
    # 1. Add two different books to cart
    client.post("/cart/add", data={"book_id": 1, "quantity": 1})
    client.post("/cart/add", data={"book_id": 2, "quantity": 2})

    # 2. Submit valid checkout form
    checkout_data = {
        "customer_name": "Jane DevOps",
        "customer_email": "jane.devops@university.edu",
        "customer_address": "Room 404, Engineering Building, College Campus",
    }
    response = client.post("/checkout", data=checkout_data, follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    # Verify confirmation page elements
    assert "Thank You for Your Order!" in html
    assert "Jane DevOps" in html
    assert "jane.devops@university.edu" in html
    assert "Docker Deep Dive" in html
    assert "The Phoenix Project" in html

    # 3. Direct database verification
    db_path = app.config["DATABASE_PATH"]
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders WHERE customer_email = ?", ("jane.devops@university.edu",))
    order_row = cursor.fetchone()
    assert order_row is not None
    assert order_row["customer_name"] == "Jane DevOps"
    assert order_row["total_amount"] > 0

    order_id = order_row["id"]
    cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    item_rows = cursor.fetchall()
    assert len(item_rows) == 2
    conn.close()

    # 4. Verify cart is now empty
    cart_resp = client.get("/cart")
    assert "Your Cart is Empty" in cart_resp.get_data(as_text=True)


def test_health_monitoring_endpoint(client):
    """Verify the /health DevOps monitoring endpoint returns healthy JSON."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert data["status"] == "healthy"
    assert data["service"] == "online-bookstore"
    assert data["database"] == "ok"


def test_idempotent_database_seeding(app):
    """
    Verify that calling init_db repeatedly does NOT duplicate records.
    Crucial for container restarts.
    """
    db_path = app.config["DATABASE_PATH"]
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS count FROM books;")
    initial_count = cursor.fetchone()["count"]
    conn.close()

    # Re-run init_db (simulating container restart)
    init_db(db_path)

    conn2 = get_db_connection(db_path)
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT COUNT(*) AS count FROM books;")
    second_count = cursor2.fetchone()["count"]
    conn2.close()

    assert initial_count == second_count
    assert initial_count == 10
