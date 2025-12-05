# Unit Tests for Stroke Patient Management System

## Overview
This test suite provides comprehensive unit tests for the Flask application, covering authentication, CRUD operations, database connectivity, and security features.

## Test Structure

### Files Created:
1. **`tests/__init__.py`** - Test package initialization
2. **`tests/conftest.py`** - Pytest configuration and fixtures
3. **`tests/test_routes.py`** - Tests for routes and business logic (39 test cases)
4. **`tests/test_config.py`** - Tests for database connectivity (15 test cases)
5. **`tests/requirements.txt`** - Test dependencies

## Test Coverage

### 1. Authentication Tests (`TestAuthentication`)
- ✅ Login page loads
- ✅ Registration page loads
- ✅ Successful user registration with password hashing
- ✅ Duplicate email prevention
- ✅ Short password rejection
- ✅ Successful login with valid credentials
- ✅ Invalid email/password handling
- ✅ Logout functionality

### 2. Dashboard Access Tests (`TestDashboardAccess`)
- ✅ Authentication required for dashboard
- ✅ Authenticated access to dashboard
- ✅ Authentication required for patient page
- ✅ Authenticated access to patient page

### 3. Patient CRUD Tests (`TestPatientCRUD`)
- ✅ Add patient page requires authentication
- ✅ Add patient with valid data
- ✅ Prevent duplicate patient IDs
- ✅ Fetch patients via API
- ✅ Fetch statistics via API
- ✅ Update existing patient
- ✅ Update nonexistent patient (error handling)
- ✅ Delete patient successfully
- ✅ Delete nonexistent patient (error handling)

### 4. Security Tests (`TestSecurityFeatures`)
- ✅ Password hashing verification (PBKDF2-SHA256)
- ✅ SQL/NoSQL injection prevention
- ✅ Session-based route protection

### 5. Input Validation Tests (`TestInputValidation`)
- ✅ Empty field rejection
- ✅ Invalid age handling
- ✅ Type conversion (string to int/float)

### 6. Database Tests (`TestDatabaseConnection` & `TestDatabaseOperations`)
- ✅ MongoDB URI configuration
- ✅ Database connection establishment
- ✅ Collection accessibility
- ✅ Query permissions
- ✅ Write permissions
- ✅ Delete permissions
- ✅ Update permissions
- ✅ Insert and find operations
- ✅ Multiple record queries

## Installation

### 1. Install test dependencies:
```powershell
pip install pytest pytest-cov
```

### 2. Or install from requirements file:
```powershell
pip install -r tests/requirements.txt
```

## Running Tests

### Run all tests:
```powershell
pytest tests/ -v
```

### Run specific test file:
```powershell
pytest tests/test_routes.py -v
pytest tests/test_config.py -v
```

### Run specific test class:
```powershell
pytest tests/test_routes.py::TestAuthentication -v
pytest tests/test_routes.py::TestPatientCRUD -v
```

### Run specific test:
```powershell
pytest tests/test_routes.py::TestAuthentication::test_successful_login -v
```

### Run with coverage report:
```powershell
pytest tests/ --cov=app --cov-report=html
```

### Run with detailed output:
```powershell
pytest tests/ -v --tb=long
```

## Test Fixtures

### `app` - Flask application instance
Creates a test Flask app with TESTING=True

### `client` - Test client
Provides a test client for making requests

### `test_user` - Test user fixture
Creates a temporary user with:
- Email: test@example.com
- Password: TestPass123
- Automatically cleaned up after test

### `test_patient` - Test patient fixture
Creates a temporary patient record (ID: 99999)
- Automatically cleaned up after test

### `authenticated_client` - Authenticated test client
Pre-authenticated client with active session

## Expected Test Results

**Total Tests:** 54 test cases
- Authentication: 8 tests
- Dashboard Access: 4 tests
- Patient CRUD: 9 tests
- Security Features: 3 tests
- Input Validation: 3 tests
- Database Connection: 9 tests
- Database Operations: 6 tests

## Notes

1. **Database Required:** Tests require active MongoDB connection
2. **Clean State:** Fixtures automatically clean up test data
3. **Isolation:** Each test runs independently
4. **Live Database:** Tests use the real database (test data is cleaned up)

## Security Verification

These tests verify:
- ✅ Passwords are hashed using PBKDF2-SHA256
- ✅ Session-based authentication protects routes
- ✅ Input validation prevents invalid data
- ✅ Duplicate prevention for users and patients
- ✅ NoSQL injection attempts are handled safely

## Troubleshooting

### If tests fail with connection errors:
- Ensure MongoDB is accessible
- Check `app/config.py` for correct MONGO_URI
- Verify network connectivity to MongoDB Atlas

### If import errors occur:
- Ensure you're in the project root directory
- Check that `app/__init__.py` has `create_app()` function

### If pytest is not found:
- Ensure pytest is installed: `pip install pytest`
- Try: `python -m pytest tests/ -v`
