"""
Flask Online Bookstore Application.
Provides catalog browsing, search/filter, shopping cart session management,
order placement, database persistence, and health monitoring endpoints.
"""

import os
import re
import uuid
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
    abort,
)
from db import get_db_connection, init_db, get_db_path


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "devops-online-bookstore-insecure-default-key"),
        DATABASE_PATH=get_db_path(),
    )

    if test_config:
        app.config.update(test_config)

    # Initialize the database on startup
    with app.app_context():
        init_db(app.config["DATABASE_PATH"])

    # Helper function to get current shopping cart from session
    def get_cart():
        if "cart" not in session or not isinstance(session["cart"], dict):
            session["cart"] = {}
        return session["cart"]

    # Context processor to inject cart count & total into all templates
    @app.context_processor
    def inject_cart_info():
        cart = get_cart()
        total_items = sum(item.get("quantity", 0) for item in cart.values())
        total_price = sum(item.get("price", 0.0) * item.get("quantity", 0) for item in cart.values())
        return {
            "cart_count": total_items,
            "cart_total": round(total_price, 2),
            "current_year": datetime.now().year,
        }

    # ------------------ Routes ------------------

    @app.route("/")
    def index():
        query = request.args.get("q", "").strip()
        selected_category = request.args.get("category", "").strip()

        conn = get_db_connection(app.config["DATABASE_PATH"])
        cursor = conn.cursor()

        # Get unique categories for filtering
        cursor.execute("SELECT DISTINCT category FROM books ORDER BY category ASC;")
        categories = [row["category"] for row in cursor.fetchall()]

        sql = "SELECT * FROM books WHERE 1=1"
        params = []

        if query:
            sql += " AND (title LIKE ? OR author LIKE ? OR description LIKE ?)"
            wildcard = f"%{query}%"
            params.extend([wildcard, wildcard, wildcard])

        if selected_category and selected_category != "All":
            sql += " AND category = ?"
            params.append(selected_category)

        sql += " ORDER BY id ASC"
        cursor.execute(sql, params)
        books = cursor.fetchall()
        conn.close()

        return render_template(
            "index.html",
            books=books,
            categories=categories,
            selected_category=selected_category,
            query=query,
        )

    @app.route("/books/<int:book_id>")
    def book_detail(book_id):
        conn = get_db_connection(app.config["DATABASE_PATH"])
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        book = cursor.fetchone()
        conn.close()

        if book is None:
            abort(404, description="Book not found")

        return render_template("book_detail.html", book=book)

    @app.route("/cart")
    def view_cart():
        cart = get_cart()
        cart_items = []
        subtotal = 0.0

        for book_id_str, item in cart.items():
            item_subtotal = item["price"] * item["quantity"]
            subtotal += item_subtotal
            cart_items.append({
                "book_id": int(book_id_str),
                "title": item["title"],
                "author": item["author"],
                "price": item["price"],
                "quantity": item["quantity"],
                "subtotal": round(item_subtotal, 2),
                "cover_color": item.get("cover_color", "#1e293b"),
                "cover_accent": item.get("cover_accent", "#38bdf8"),
            })

        subtotal = round(subtotal, 2)
        return render_template("cart.html", cart_items=cart_items, subtotal=subtotal)

    @app.route("/cart/add", methods=["POST"])
    def add_to_cart():
        try:
            book_id = int(request.form.get("book_id", 0))
            quantity = int(request.form.get("quantity", 1))
        except (ValueError, TypeError):
            flash("Invalid book or quantity specified.", "error")
            return redirect(url_for("index"))

        if quantity <= 0:
            quantity = 1

        conn = get_db_connection(app.config["DATABASE_PATH"])
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        book = cursor.fetchone()
        conn.close()

        if not book:
            flash("The selected book could not be found.", "error")
            return redirect(url_for("index"))

        cart = get_cart()
        book_key = str(book_id)

        if book_key in cart:
            cart[book_key]["quantity"] += quantity
        else:
            cart[book_key] = {
                "title": book["title"],
                "author": book["author"],
                "price": float(book["price"]),
                "quantity": quantity,
                "cover_color": book["cover_color"],
                "cover_accent": book["cover_accent"],
            }

        session.modified = True
        flash(f"'{book['title']}' added to your shopping cart!", "success")

        next_page = request.form.get("next")
        if next_page and next_page.startswith("/"):
            return redirect(next_page)
        return redirect(url_for("view_cart"))

    @app.route("/cart/update", methods=["POST"])
    def update_cart():
        book_id = request.form.get("book_id")
        action = request.form.get("action")
        cart = get_cart()

        if not book_id or book_id not in cart:
            flash("Item not found in your cart.", "error")
            return redirect(url_for("view_cart"))

        if action == "increase":
            cart[book_id]["quantity"] += 1
            flash(f"Updated quantity for '{cart[book_id]['title']}'.", "info")
        elif action == "decrease":
            cart[book_id]["quantity"] -= 1
            if cart[book_id]["quantity"] <= 0:
                removed_title = cart[book_id]["title"]
                del cart[book_id]
                flash(f"Removed '{removed_title}' from cart.", "info")
            else:
                flash(f"Updated quantity for '{cart[book_id]['title']}'.", "info")
        elif action == "remove":
            removed_title = cart[book_id]["title"]
            del cart[book_id]
            flash(f"Removed '{removed_title}' from cart.", "info")

        session.modified = True
        return redirect(url_for("view_cart"))

    @app.route("/cart/clear", methods=["POST"])
    def clear_cart():
        session["cart"] = {}
        session.modified = True
        flash("Your shopping cart has been cleared.", "info")
        return redirect(url_for("view_cart"))

    @app.route("/checkout", methods=["GET", "POST"])
    def checkout():
        cart = get_cart()
        if not cart:
            flash("Your cart is empty. Please add books before proceeding to checkout.", "warning")
            return redirect(url_for("index"))

        subtotal = round(sum(item["price"] * item["quantity"] for item in cart.values()), 2)
        total_items = sum(item["quantity"] for item in cart.values())

        if request.method == "POST":
            customer_name = request.form.get("customer_name", "").strip()
            customer_email = request.form.get("customer_email", "").strip()
            customer_address = request.form.get("customer_address", "").strip()

            errors = []
            if not customer_name:
                errors.append("Full Name is required.")
            if not customer_email:
                errors.append("Email Address is required.")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", customer_email):
                errors.append("Please enter a valid email address.")
            if not customer_address:
                errors.append("Shipping Address is required.")

            if errors:
                for err in errors:
                    flash(err, "error")
                return render_template(
                    "checkout.html",
                    cart_items=cart.values(),
                    subtotal=subtotal,
                    customer_name=customer_name,
                    customer_email=customer_email,
                    customer_address=customer_address,
                )

            # Generate unique order reference
            order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

            conn = get_db_connection(app.config["DATABASE_PATH"])
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO orders (order_number, customer_name, customer_email, customer_address, total_amount, item_count)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (order_number, customer_name, customer_email, customer_address, subtotal, total_items),
            )
            order_id = cursor.lastrowid

            for book_id_str, item in cart.items():
                item_subtotal = round(item["price"] * item["quantity"], 2)
                cursor.execute(
                    """
                    INSERT INTO order_items (order_id, book_id, book_title, unit_price, quantity, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """,
                    (order_id, int(book_id_str), item["title"], item["price"], item["quantity"], item_subtotal),
                )

            conn.commit()
            conn.close()

            # Empty session cart
            session["cart"] = {}
            session.modified = True

            flash("Order placed successfully! Thank you for your purchase.", "success")
            return redirect(url_for("order_confirmation", order_number=order_number))

        return render_template("checkout.html", cart_items=cart.values(), subtotal=subtotal)

    @app.route("/order-confirmation/<order_number>")
    def order_confirmation(order_number):
        conn = get_db_connection(app.config["DATABASE_PATH"])
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM orders WHERE order_number = ?", (order_number,))
        order = cursor.fetchone()

        if not order:
            conn.close()
            abort(404, description="Order not found")

        cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order["id"],))
        items = cursor.fetchall()
        conn.close()

        return render_template("confirmation.html", order=order, items=items)

    @app.route("/health")
    def health_check():
        db_status = "ok"
        try:
            conn = get_db_connection(app.config["DATABASE_PATH"])
            conn.execute("SELECT 1;").fetchone()
            conn.close()
        except Exception as e:
            db_status = f"error: {str(e)}"

        status_code = 200 if db_status == "ok" else 503
        return jsonify({
            "status": "healthy" if db_status == "ok" else "unhealthy",
            "service": "online-bookstore",
            "version": "1.0.0",
            "database": db_status,
        }), status_code

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html", error=e), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("500.html", error=e), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
