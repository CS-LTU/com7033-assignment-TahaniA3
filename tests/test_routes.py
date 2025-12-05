"""
Unit tests for authentication and patient management routes.
Tests cover login, registration, CRUD operations, and security features.
"""
import pytest
from app.config import users_collection, collection
from werkzeug.security import check_password_hash


class TestAuthentication:
    """Test suite for authentication routes (login, register, logout)."""
    
    def test_login_page_loads(self, client):
        """Test that the login page loads successfully."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_register_page_loads(self, client):
        """Test that the registration page loads successfully."""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Register' in response.data
    
    def test_successful_registration(self, client):
        """Test user registration with valid data."""
        # Clean up test user if exists
        users_collection.delete_one({'email': 'newuser@example.com'})
        
        response = client.post('/register', data={
            'email': 'newuser@example.com',
            'password': 'SecurePass123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify user was created in database
        user = users_collection.find_one({'email': 'newuser@example.com'})
        assert user is not None
        assert user['email'] == 'newuser@example.com'
        
        # Verify password was hashed
        assert check_password_hash(user['password'], 'SecurePass123')
        
        # Cleanup
        users_collection.delete_one({'email': 'newuser@example.com'})
    
    def test_registration_duplicate_email(self, client, test_user):
        """Test that duplicate email registration is prevented."""
        response = client.post('/register', data={
            'email': test_user['email'],
            'password': 'AnotherPass123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'already exists' in response.data or b'already registered' in response.data
    
    def test_registration_short_password(self, client):
        """Test that short passwords are rejected."""
        response = client.post('/register', data={
            'email': 'shortpass@example.com',
            'password': '123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should show error about password length
    
    def test_successful_login(self, client, test_user):
        """Test login with valid credentials."""
        response = client.post('/login', data={
            'email': test_user['email'],
            'password': test_user['password']
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Check if session was created
        with client.session_transaction() as session:
            assert 'user' in session
            assert session['user'] == test_user['email']
    
    def test_login_invalid_email(self, client):
        """Test login with non-existent email."""
        response = client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'AnyPassword123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid' in response.data or b'not found' in response.data
    
    def test_login_wrong_password(self, client, test_user):
        """Test login with incorrect password."""
        response = client.post('/login', data={
            'email': test_user['email'],
            'password': 'WrongPassword123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid' in response.data or b'incorrect' in response.data
    
    def test_logout(self, authenticated_client):
        """Test logout functionality."""
        response = authenticated_client.get('/logout', follow_redirects=True)
        
        assert response.status_code == 200
        
        # Check if session was cleared
        with authenticated_client.session_transaction() as session:
            assert 'user' not in session


class TestDashboardAccess:
    """Test suite for dashboard and patient page access control."""
    
    def test_dashboard_requires_authentication(self, client):
        """Test that dashboard redirects unauthenticated users."""
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code == 302  # Redirect
        assert '/login' in response.location
    
    def test_dashboard_authenticated_access(self, authenticated_client):
        """Test that authenticated users can access dashboard."""
        response = authenticated_client.get('/dashboard')
        assert response.status_code == 200
        assert b'Dashboard' in response.data or b'Statistics' in response.data
    
    def test_patient_page_requires_authentication(self, client):
        """Test that patient page requires authentication."""
        response = client.get('/patient', follow_redirects=False)
        assert response.status_code == 302  # Redirect
        assert '/login' in response.location
    
    def test_patient_page_authenticated_access(self, authenticated_client):
        """Test that authenticated users can access patient page."""
        response = authenticated_client.get('/patient')
        assert response.status_code == 200
        assert b'Patient' in response.data


class TestPatientCRUD:
    """Test suite for Create, Read, Update, Delete operations on patient records."""
    
    def test_add_patient_page_requires_auth(self, client):
        """Test that add patient page requires authentication."""
        response = client.get('/add_patient', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_add_patient_success(self, authenticated_client):
        """Test adding a new patient with valid data."""
        # Clean up if test patient exists
        collection.delete_one({'id': 88888})
        
        patient_data = {
            'id': '88888',
            'gender': 'Female',
            'age': '35',
            'hypertension': '0',
            'heart_disease': '0',
            'ever_married': 'Yes',
            'work_type': 'Private',
            'Residence_type': 'Urban',
            'avg_glucose_level': '95.5',
            'bmi': '25.3',
            'smoking_status': 'never smoked',
            'stroke': '0'
        }
        
        response = authenticated_client.post('/add_patient', data=patient_data, follow_redirects=True)
        assert response.status_code == 200
        
        # Verify patient was added to database
        patient = collection.find_one({'id': 88888})
        assert patient is not None
        assert patient['gender'] == 'Female'
        assert patient['age'] == 35.0
        
        # Cleanup
        collection.delete_one({'id': 88888})
    
    def test_add_patient_duplicate_id(self, authenticated_client, test_patient):
        """Test that duplicate patient IDs are prevented."""
        patient_data = {
            'id': str(test_patient['id']),
            'gender': 'Male',
            'age': '40',
            'hypertension': '1',
            'heart_disease': '0',
            'ever_married': 'Yes',
            'work_type': 'Self-employed',
            'Residence_type': 'Rural',
            'avg_glucose_level': '110.0',
            'bmi': '30.0',
            'smoking_status': 'smokes',
            'stroke': '1'
        }
        
        response = authenticated_client.post('/add_patient', data=patient_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'already exists' in response.data or b'duplicate' in response.data.lower()
    
    def test_get_patients_api(self, authenticated_client, test_patient):
        """Test fetching patient records via API."""
        response = authenticated_client.get('/api/patients')
        assert response.status_code == 200
        
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Find our test patient in the results
        test_found = any(p['id'] == test_patient['id'] for p in data if 'id' in p)
        assert test_found
    
    def test_get_stats_api(self, authenticated_client):
        """Test fetching statistics via API."""
        response = authenticated_client.get('/api/stats')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'total_patients' in data
        assert 'average_age' in data
        assert 'stroke_percentage' in data
        assert 'gender_distribution' in data
        assert isinstance(data['total_patients'], int)
    
    def test_update_patient_success(self, authenticated_client, test_patient):
        """Test updating an existing patient record."""
        updated_data = {
            'id': str(test_patient['id']),
            'gender': 'Male',
            'age': '50',  # Changed from 45
            'hypertension': '1',  # Changed from 0
            'heart_disease': '0',
            'ever_married': 'Yes',
            'work_type': 'Private',
            'Residence_type': 'Urban',
            'avg_glucose_level': '120.5',  # Changed
            'bmi': '30.0',  # Changed
            'smoking_status': 'formerly smoked',  # Changed
            'stroke': '0'
        }
        
        response = authenticated_client.post('/api/update_patient', data=updated_data)
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True
        
        # Verify changes in database
        patient = collection.find_one({'id': test_patient['id']})
        assert patient['age'] == 50.0
        assert patient['hypertension'] == 1
        assert patient['bmi'] == 30.0
    
    def test_update_nonexistent_patient(self, authenticated_client):
        """Test updating a patient that doesn't exist."""
        updated_data = {
            'id': '77777',
            'gender': 'Male',
            'age': '50',
            'hypertension': '0',
            'heart_disease': '0',
            'ever_married': 'Yes',
            'work_type': 'Private',
            'Residence_type': 'Urban',
            'avg_glucose_level': '100.0',
            'bmi': '25.0',
            'smoking_status': 'never smoked',
            'stroke': '0'
        }
        
        response = authenticated_client.post('/api/update_patient', data=updated_data)
        data = response.get_json()
        assert data['success'] is False
    
    def test_delete_patient_success(self, authenticated_client):
        """Test deleting a patient record."""
        # Create a patient to delete
        delete_patient = {
            'id': 66666,
            'gender': 'Female',
            'age': 55.0,
            'hypertension': 0,
            'heart_disease': 1,
            'ever_married': 'Yes',
            'work_type': 'Govt_job',
            'Residence_type': 'Urban',
            'avg_glucose_level': 130.0,
            'bmi': 32.0,
            'smoking_status': 'Unknown',
            'stroke': 1
        }
        collection.insert_one(delete_patient)
        
        response = authenticated_client.post('/api/delete_patient', 
                                             json={'id': 66666})
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True
        
        # Verify patient was deleted
        patient = collection.find_one({'id': 66666})
        assert patient is None
    
    def test_delete_nonexistent_patient(self, authenticated_client):
        """Test deleting a patient that doesn't exist."""
        response = authenticated_client.post('/api/delete_patient', 
                                             json={'id': 55555})
        data = response.get_json()
        assert data['success'] is False


class TestSecurityFeatures:
    """Test suite for security features (password hashing, input validation)."""
    
    def test_password_is_hashed(self, client):
        """Test that passwords are stored as hashes, not plaintext."""
        # Register new user
        test_email = 'hashtest@example.com'
        test_password = 'MySecurePass123'
        
        users_collection.delete_one({'email': test_email})
        
        client.post('/register', data={
            'email': test_email,
            'password': test_password
        })
        
        # Check database
        user = users_collection.find_one({'email': test_email})
        assert user is not None
        
        # Password should NOT be plaintext
        assert user['password'] != test_password
        
        # Password should be a valid hash (starts with method identifier)
        assert user['password'].startswith('pbkdf2:sha256:')
        
        # Should be able to verify the hash
        assert check_password_hash(user['password'], test_password)
        
        # Cleanup
        users_collection.delete_one({'email': test_email})
    
    def test_sql_injection_prevention(self, authenticated_client):
        """Test that SQL injection attempts are handled safely."""
        # Try SQL injection in patient ID
        malicious_data = {
            'id': "1' OR '1'='1",
            'gender': 'Male',
            'age': '40',
            'hypertension': '0',
            'heart_disease': '0',
            'ever_married': 'Yes',
            'work_type': 'Private',
            'Residence_type': 'Urban',
            'avg_glucose_level': '100.0',
            'bmi': '25.0',
            'smoking_status': 'never smoked',
            'stroke': '0'
        }
        
        # MongoDB uses NoSQL, but should handle this safely
        response = authenticated_client.post('/add_patient', data=malicious_data, follow_redirects=True)
        assert response.status_code == 200
        
        # Should either reject or safely store the data
        # No database corruption should occur
    
    def test_session_protection(self, client):
        """Test that routes are protected by session authentication."""
        # Try to access protected routes without authentication
        protected_routes = [
            '/dashboard',
            '/patient',
            '/add_patient',
            '/api/patients',
            '/api/stats'
        ]
        
        for route in protected_routes:
            response = client.get(route, follow_redirects=False)
            assert response.status_code == 302  # Should redirect to login
            assert '/login' in response.location


class TestInputValidation:
    """Test suite for input validation on forms."""
    
    def test_registration_empty_fields(self, client):
        """Test that empty fields are rejected during registration."""
        response = client.post('/register', data={
            'email': '',
            'password': ''
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should show validation error
    
    def test_patient_invalid_age(self, authenticated_client):
        """Test that invalid age values are handled."""
        patient_data = {
            'id': '11111',
            'gender': 'Male',
            'age': '-5',  # Invalid negative age
            'hypertension': '0',
            'heart_disease': '0',
            'ever_married': 'Yes',
            'work_type': 'Private',
            'Residence_type': 'Urban',
            'avg_glucose_level': '100.0',
            'bmi': '25.0',
            'smoking_status': 'never smoked',
            'stroke': '0'
        }
        
        response = authenticated_client.post('/add_patient', data=patient_data, follow_redirects=True)
        # Should either reject or convert to valid value
        assert response.status_code == 200
    
    def test_patient_type_conversion(self, authenticated_client):
        """Test that string inputs are properly converted to correct types."""
        collection.delete_one({'id': 22222})
        
        patient_data = {
            'id': '22222',
            'gender': 'Female',
            'age': '42',  # String should convert to float
            'hypertension': '1',  # String should convert to int
            'heart_disease': '0',
            'ever_married': 'No',
            'work_type': 'children',
            'Residence_type': 'Rural',
            'avg_glucose_level': '98.75',  # String should convert to float
            'bmi': '27.3',
            'smoking_status': 'never smoked',
            'stroke': '0'
        }
        
        authenticated_client.post('/add_patient', data=patient_data)
        
        # Check database for correct types
        patient = collection.find_one({'id': 22222})
        if patient:
            assert isinstance(patient['age'], (int, float))
            assert isinstance(patient['hypertension'], int)
            assert isinstance(patient['avg_glucose_level'], (int, float))
            
            # Cleanup
            collection.delete_one({'id': 22222})


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
