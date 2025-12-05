"""
Database Manager for Multiple Interconnected Databases
Handles operations across user management, patient records, and audit databases
"""
from datetime import datetime
from app.config import (
    users_collection, user_sessions_collection,
    collection, patient_history_collection,
    access_logs_collection, data_changes_collection
)


class DatabaseManager:
    """Manages operations across multiple interconnected databases."""
    
    @staticmethod
    def log_access(user_email, action, resource, details=None):
        """
        Log user access to audit database.
        Creates interconnection between user_management_db and audit_logs_db.
        """
        log_entry = {
            'user_email': user_email,
            'action': action,  # e.g., 'login', 'view_patient', 'update_patient'
            'resource': resource,  # e.g., 'dashboard', 'patient_id:12345'
            'timestamp': datetime.utcnow(),
            'details': details or {}
        }
        access_logs_collection.insert_one(log_entry)
        return log_entry
    
    @staticmethod
    def log_data_change(user_email, operation, database, collection_name, record_id, old_data=None, new_data=None):
        """
        Log data modifications to audit database.
        Tracks all CRUD operations across patient and user databases.
        """
        change_entry = {
            'user_email': user_email,
            'operation': operation,  # 'CREATE', 'READ', 'UPDATE', 'DELETE'
            'database': database,  # 'user_management_db', 'stroke_patient_db'
            'collection': collection_name,
            'record_id': record_id,
            'old_data': old_data,
            'new_data': new_data,
            'timestamp': datetime.utcnow()
        }
        data_changes_collection.insert_one(change_entry)
        return change_entry
    
    @staticmethod
    def create_user_session(user_email, session_id):
        """
        Create session record in user management database.
        Links user authentication to session tracking.
        """
        session_data = {
            'user_email': user_email,
            'session_id': session_id,
            'login_time': datetime.utcnow(),
            'last_activity': datetime.utcnow(),
            'active': True
        }
        user_sessions_collection.insert_one(session_data)
        
        # Log this access across databases
        DatabaseManager.log_access(user_email, 'login', 'system', 
                                   {'session_id': session_id})
        return session_data
    
    @staticmethod
    def end_user_session(user_email, session_id):
        """
        End user session and log to audit database.
        Demonstrates interconnection between databases.
        """
        user_sessions_collection.update_one(
            {'user_email': user_email, 'session_id': session_id},
            {'$set': {'active': False, 'logout_time': datetime.utcnow()}}
        )
        
        # Log logout across databases
        DatabaseManager.log_access(user_email, 'logout', 'system',
                                   {'session_id': session_id})
    
    @staticmethod
    def add_patient_with_audit(user_email, patient_data):
        """
        Add patient to patient database and log to audit database.
        Demonstrates interconnected database operations.
        """
        # Insert into patient database
        result = collection.insert_one(patient_data)
        
        # Log to audit database
        DatabaseManager.log_data_change(
            user_email=user_email,
            operation='CREATE',
            database='stroke_patient_db',
            collection_name='patients',
            record_id=patient_data.get('id'),
            new_data=patient_data
        )
        
        # Log access
        DatabaseManager.log_access(
            user_email, 'create_patient', f"patient_id:{patient_data.get('id')}"
        )
        
        return result
    
    @staticmethod
    def update_patient_with_history(user_email, patient_id, old_data, new_data):
        """
        Update patient in patient database, save history, and audit.
        Demonstrates data flow across multiple databases.
        """
        # Update in patient database
        result = collection.update_one(
            {'id': patient_id},
            {'$set': new_data}
        )
        
        # Save history in patient database
        history_entry = {
            'patient_id': patient_id,
            'modified_by': user_email,
            'modified_at': datetime.utcnow(),
            'old_data': old_data,
            'new_data': new_data
        }
        patient_history_collection.insert_one(history_entry)
        
        # Log change in audit database
        DatabaseManager.log_data_change(
            user_email=user_email,
            operation='UPDATE',
            database='stroke_patient_db',
            collection_name='patients',
            record_id=patient_id,
            old_data=old_data,
            new_data=new_data
        )
        
        # Log access
        DatabaseManager.log_access(
            user_email, 'update_patient', f"patient_id:{patient_id}"
        )
        
        return result
    
    @staticmethod
    def delete_patient_with_audit(user_email, patient_id):
        """
        Delete patient and maintain audit trail across databases.
        """
        # Get patient data before deletion
        patient_data = collection.find_one({'id': patient_id})
        
        if patient_data:
            # Delete from patient database
            result = collection.delete_one({'id': patient_id})
            
            # Log deletion in audit database
            DatabaseManager.log_data_change(
                user_email=user_email,
                operation='DELETE',
                database='stroke_patient_db',
                collection_name='patients',
                record_id=patient_id,
                old_data=patient_data
            )
            
            # Log access
            DatabaseManager.log_access(
                user_email, 'delete_patient', f"patient_id:{patient_id}"
            )
            
            return result
        return None
    
    @staticmethod
    def get_user_activity_report(user_email):
        """
        Generate cross-database report of user activities.
        Queries both user management and audit databases.
        """
        # Get user info from user management database
        user = users_collection.find_one({'email': user_email})
        
        # Get sessions from user management database
        sessions = list(user_sessions_collection.find({'user_email': user_email}))
        
        # Get access logs from audit database
        access_logs = list(access_logs_collection.find(
            {'user_email': user_email}
        ).sort('timestamp', -1).limit(50))
        
        # Get data changes from audit database
        data_changes = list(data_changes_collection.find(
            {'user_email': user_email}
        ).sort('timestamp', -1).limit(50))
        
        return {
            'user': user,
            'sessions': sessions,
            'access_logs': access_logs,
            'data_changes': data_changes
        }
    
    @staticmethod
    def get_patient_full_history(patient_id):
        """
        Get complete patient history across databases.
        Retrieves current data and all historical changes.
        """
        # Current data from patient database
        current_data = collection.find_one({'id': patient_id})
        
        # Historical changes from patient database
        history = list(patient_history_collection.find(
            {'patient_id': patient_id}
        ).sort('modified_at', -1))
        
        # Audit trail from audit database
        audit_trail = list(data_changes_collection.find(
            {'record_id': patient_id, 'database': 'stroke_patient_db'}
        ).sort('timestamp', -1))
        
        return {
            'current_data': current_data,
            'history': history,
            'audit_trail': audit_trail
        }
    
    @staticmethod
    def verify_database_connections():
        """
        Verify all three databases are accessible and connected.
        """
        try:
            # Test user management database
            users_collection.count_documents({})
            user_sessions_collection.count_documents({})
            
            # Test patient database
            collection.count_documents({})
            patient_history_collection.count_documents({})
            
            # Test audit database
            access_logs_collection.count_documents({})
            data_changes_collection.count_documents({})
            
            return {
                'status': 'success',
                'message': 'All three databases connected successfully',
                'databases': {
                    'user_management_db': 'connected',
                    'stroke_patient_db': 'connected',
                    'audit_logs_db': 'connected'
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
