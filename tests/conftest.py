"""
Pytest configuration and fixtures for testing the Flask application.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.config import collection, users_collection
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Create and configure a test Flask application instance."""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the Flask application."""
    return app.test_cli_runner()


@pytest.fixture
def test_user():
    """Create a test user in the database and clean up after test."""
    # Create test user
    test_email = "test@example.com"
    test_password = "TestPass123"
    
    user_data = {
        'email': test_email,
        'password': generate_password_hash(test_password)
    }
    
    # Clean up if exists
    users_collection.delete_one({'email': test_email})
    
    # Insert test user
    users_collection.insert_one(user_data)
    
    yield {'email': test_email, 'password': test_password}
    
    # Cleanup after test
    users_collection.delete_one({'email': test_email})


@pytest.fixture
def test_patient():
    """Create a test patient record and clean up after test."""
    patient_data = {
        'id': 99999,
        'gender': 'Male',
        'age': 45.0,
        'hypertension': 0,
        'heart_disease': 0,
        'ever_married': 'Yes',
        'work_type': 'Private',
        'Residence_type': 'Urban',
        'avg_glucose_level': 105.5,
        'bmi': 28.5,
        'smoking_status': 'never smoked',
        'stroke': 0
    }
    
    # Clean up if exists
    collection.delete_one({'id': 99999})
    
    # Insert test patient
    collection.insert_one(patient_data)
    
    yield patient_data
    
    # Cleanup after test
    collection.delete_one({'id': 99999})


@pytest.fixture
def authenticated_client(client, test_user):
    """Create an authenticated test client with session."""
    with client.session_transaction() as session:
        session['user'] = test_user['email']
    return client
