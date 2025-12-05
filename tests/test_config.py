"""
Unit tests for database configuration and connectivity.
Tests MongoDB connection and collection operations.
"""
import pytest
from app.config import client, db, collection, users_collection, MONGO_URI


class TestDatabaseConnection:
    """Test suite for MongoDB connection and configuration."""
    
    def test_mongo_uri_exists(self):
        """Test that MongoDB URI is properly configured."""
        assert MONGO_URI is not None
        assert isinstance(MONGO_URI, str)
        assert 'mongodb' in MONGO_URI.lower()
    
    def test_database_connection(self):
        """Test that database connection is established."""
        assert client is not None
        assert db is not None
    
    def test_collections_exist(self):
        """Test that required collections are accessible."""
        assert collection is not None
        assert users_collection is not None
    
    def test_can_query_collection(self):
        """Test that we can query the stroke_collection."""
        try:
            # Attempt to count documents
            count = collection.count_documents({})
            assert count >= 0  # Should return non-negative number
        except Exception as e:
            pytest.fail(f"Failed to query collection: {e}")
    
    def test_can_query_users_collection(self):
        """Test that we can query the users collection."""
        try:
            # Attempt to count documents
            count = users_collection.count_documents({})
            assert count >= 0  # Should return non-negative number
        except Exception as e:
            pytest.fail(f"Failed to query users collection: {e}")
    
    def test_database_write_permission(self):
        """Test that we have write permissions to the database."""
        test_doc = {'test_key': 'test_value', 'test_id': 'pytest_temp'}
        
        try:
            # Insert test document
            result = collection.insert_one(test_doc)
            assert result.inserted_id is not None
            
            # Verify insertion
            found = collection.find_one({'test_id': 'pytest_temp'})
            assert found is not None
            assert found['test_key'] == 'test_value'
            
        finally:
            # Cleanup
            collection.delete_one({'test_id': 'pytest_temp'})
    
    def test_database_delete_permission(self):
        """Test that we have delete permissions to the database."""
        test_doc = {'test_key': 'delete_test', 'test_id': 'pytest_delete'}
        
        try:
            # Insert test document
            collection.insert_one(test_doc)
            
            # Delete test document
            result = collection.delete_one({'test_id': 'pytest_delete'})
            assert result.deleted_count == 1
            
            # Verify deletion
            found = collection.find_one({'test_id': 'pytest_delete'})
            assert found is None
            
        except Exception as e:
            pytest.fail(f"Failed to delete document: {e}")
    
    def test_database_update_permission(self):
        """Test that we have update permissions to the database."""
        test_doc = {'test_key': 'original', 'test_id': 'pytest_update'}
        
        try:
            # Insert test document
            collection.insert_one(test_doc)
            
            # Update test document
            result = collection.update_one(
                {'test_id': 'pytest_update'},
                {'$set': {'test_key': 'updated'}}
            )
            assert result.modified_count == 1
            
            # Verify update
            found = collection.find_one({'test_id': 'pytest_update'})
            assert found is not None
            assert found['test_key'] == 'updated'
            
        finally:
            # Cleanup
            collection.delete_one({'test_id': 'pytest_update'})


class TestDatabaseOperations:
    """Test suite for database CRUD operations."""
    
    def test_insert_and_find_patient(self):
        """Test inserting and finding a patient record."""
        patient_data = {
            'id': 99998,
            'gender': 'Male',
            'age': 60.0,
            'hypertension': 1,
            'heart_disease': 0,
            'ever_married': 'Yes',
            'work_type': 'Self-employed',
            'Residence_type': 'Rural',
            'avg_glucose_level': 115.0,
            'bmi': 29.5,
            'smoking_status': 'smokes',
            'stroke': 0
        }
        
        try:
            # Insert
            collection.insert_one(patient_data)
            
            # Find
            found = collection.find_one({'id': 99998})
            assert found is not None
            assert found['gender'] == 'Male'
            assert found['age'] == 60.0
            assert found['hypertension'] == 1
            
        finally:
            # Cleanup
            collection.delete_one({'id': 99998})
    
    def test_update_patient_record(self):
        """Test updating a patient record."""
        patient_data = {
            'id': 99997,
            'gender': 'Female',
            'age': 55.0,
            'bmi': 25.0,
            'stroke': 0
        }
        
        try:
            # Insert
            collection.insert_one(patient_data)
            
            # Update
            collection.update_one(
                {'id': 99997},
                {'$set': {'age': 56.0, 'bmi': 26.0}}
            )
            
            # Verify
            updated = collection.find_one({'id': 99997})
            assert updated['age'] == 56.0
            assert updated['bmi'] == 26.0
            
        finally:
            # Cleanup
            collection.delete_one({'id': 99997})
    
    def test_delete_patient_record(self):
        """Test deleting a patient record."""
        patient_data = {
            'id': 99996,
            'gender': 'Male',
            'age': 70.0
        }
        
        # Insert
        collection.insert_one(patient_data)
        
        # Verify exists
        found = collection.find_one({'id': 99996})
        assert found is not None
        
        # Delete
        result = collection.delete_one({'id': 99996})
        assert result.deleted_count == 1
        
        # Verify deleted
        not_found = collection.find_one({'id': 99996})
        assert not_found is None
    
    def test_insert_and_find_user(self):
        """Test inserting and finding a user record."""
        from werkzeug.security import generate_password_hash
        
        user_data = {
            'email': 'dbtest@example.com',
            'password': generate_password_hash('TestPassword123')
        }
        
        try:
            # Insert
            users_collection.insert_one(user_data)
            
            # Find
            found = users_collection.find_one({'email': 'dbtest@example.com'})
            assert found is not None
            assert found['email'] == 'dbtest@example.com'
            assert 'password' in found
            
        finally:
            # Cleanup
            users_collection.delete_one({'email': 'dbtest@example.com'})
    
    def test_find_multiple_patients(self):
        """Test querying multiple patient records."""
        # This test assumes some data exists in the database
        patients = list(collection.find().limit(5))
        assert isinstance(patients, list)
        # If database has data, should return records
        # If empty, should return empty list
        assert len(patients) >= 0
    
    def test_count_documents(self):
        """Test counting documents in collections."""
        patient_count = collection.count_documents({})
        user_count = users_collection.count_documents({})
        
        assert isinstance(patient_count, int)
        assert isinstance(user_count, int)
        assert patient_count >= 0
        assert user_count >= 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
