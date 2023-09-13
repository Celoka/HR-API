# tests/conftest.py

import pytest
from app import app, db

# Create a test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Clean the database after each test
@pytest.fixture(autouse=True)
def cleanup_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
