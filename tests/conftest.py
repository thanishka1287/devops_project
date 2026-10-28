"""
Pytest configuration and shared fixtures.
Sets up an isolated SQLite test database for each test session or function.
"""

import os
import tempfile
import pytest
from app import create_app
from db import get_db_connection


@pytest.fixture
def app(tmp_path):
    """
    Creates and configures a unique isolated Flask application instance
    with a separate temporary SQLite database for test execution.
    """
    db_file = tmp_path / "test_bookstore.db"
    test_config = {
        "TESTING": True,
        "DATABASE_PATH": str(db_file),
        "SECRET_KEY": "devops-testing-secret-key-123",
        "WTF_CSRF_ENABLED": False,
    }

    application = create_app(test_config=test_config)
    yield application


@pytest.fixture
def client(app):
    """
    Flask test client fixture to simulate HTTP requests.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Flask CLI runner fixture.
    """
    return app.test_cli_runner()
