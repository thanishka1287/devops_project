"""
Database initialization and connection management for Online Bookstore.
Handles SQLite connection, schema creation, and idempotency seeding.
"""

import os
import sqlite3

DEFAULT_DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DEFAULT_DB_PATH = os.path.join(DEFAULT_DB_DIR, "bookstore.db")


def get_db_path(custom_path=None):
    """
    Determine the database file path from parameter, environment variable,
    or project default location.
    """
    if custom_path:
        return custom_path
    env_path = os.environ.get("DATABASE_PATH")
    if env_path:
        return env_path
    return DEFAULT_DB_PATH


def get_db_connection(db_path=None):
    """
    Open and return a configured connection to the SQLite database.
    Row factory is enabled for dictionary-like column access.
    """
    resolved_path = get_db_path(db_path)
    os.makedirs(os.path.dirname(os.path.abspath(resolved_path)), exist_ok=True)
    conn = sqlite3.connect(resolved_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path=None):
    """
    Create necessary tables if they do not exist and seed initial book inventory.
    Guarantees no duplicate sample books on repeated restarts.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # Books Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            stock INTEGER NOT NULL DEFAULT 15,
            cover_color TEXT NOT NULL DEFAULT '#1e293b',
            cover_accent TEXT NOT NULL DEFAULT '#38bdf8',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_address TEXT NOT NULL,
            total_amount REAL NOT NULL,
            item_count INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Order Items Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            book_title TEXT NOT NULL,
            unit_price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books (id)
        );
    """)

    conn.commit()

    # Seed sample books if database is empty
    seed_sample_books(conn)
    conn.close()


def seed_sample_books(conn):
    """
    Seed initial books catalogue only if the books table is empty.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS count FROM books;")
    row = cursor.fetchone()

    if row and row["count"] == 0:
        sample_books = [
            (
                "Docker Deep Dive",
                "Nigel Poulton",
                "DevOps & Cloud",
                34.99,
                "Master Docker from fundamentals to production orchestration, containers, images, and multi-host networking.",
                "978-1521822807",
                25,
                "#0f172a",
                "#0284c7",
            ),
            (
                "The Phoenix Project",
                "Gene Kim, Kevin Behr & George Spafford",
                "DevOps & Cloud",
                29.99,
                "A novel about IT, DevOps, and helping your business win in the fast-paced modern technology landscape.",
                "978-0988262591",
                20,
                "#1e1b4b",
                "#6366f1",
            ),
            (
                "Continuous Delivery",
                "Jez Humble & David Farley",
                "DevOps & Cloud",
                39.99,
                "Reliable software releases through build, test, and deployment automation with modern CI/CD pipelines.",
                "978-0321601919",
                15,
                "#14532d",
                "#22c55e",
            ),
            (
                "Clean Code",
                "Robert C. Martin",
                "Software Engineering",
                36.50,
                "A handbook of agile software craftsmanship with practical principles of writing readable, maintainable code.",
                "978-0132350884",
                30,
                "#701a75",
                "#d946ef",
            ),
            (
                "Designing Data-Intensive Applications",
                "Martin Kleppmann",
                "Software Engineering",
                44.95,
                "The definitive guide to data systems, scalability, consistency, reliability, and distributed systems architecture.",
                "978-1449373320",
                18,
                "#7c2d12",
                "#f97316",
            ),
            (
                "Flask Web Development",
                "Miguel Grinberg",
                "Web Development",
                32.00,
                "Developing full-featured web applications with Python, Flask, Jinja templates, and database integrations.",
                "978-1491991732",
                22,
                "#064e3b",
                "#10b981",
            ),
            (
                "Fluent Python",
                "Luciano Ramalho",
                "Computer Science",
                42.50,
                "Clear, concise, and effective programming guide diving deep into idiomatic Python features and data models.",
                "978-1491946008",
                14,
                "#1e3a8a",
                "#3b82f6",
            ),
            (
                "Site Reliability Engineering",
                "Betsy Beyer, Chris Jones, Jennifer Petoff & Niall Richard Murphy",
                "DevOps & Cloud",
                38.00,
                "How Google runs production systems: SLAs, monitoring, emergency response, and infrastructure engineering.",
                "978-1491929124",
                19,
                "#111827",
                "#e11d48",
            ),
            (
                "Introduction to Algorithms (CLRS)",
                "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest & Clifford Stein",
                "Computer Science",
                59.99,
                "Comprehensive textbook covering modern algorithmic analysis, graph theory, data structures, and dynamic programming.",
                "978-0262033848",
                12,
                "#312e81",
                "#818cf8",
            ),
            (
                "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow",
                "Aurélien Géron",
                "Data Science",
                48.50,
                "Practical guide to building intelligent systems using state-of-the-art Python machine learning libraries.",
                "978-1492032649",
                16,
                "#831843",
                "#ec4899",
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO books (title, author, category, price, description, isbn, stock, cover_color, cover_accent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            sample_books,
        )
        conn.commit()
