"""
Migration Script for Multiple Interconnected Databases
Sets up three separate databases with proper structure and relationships
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import (
    client,
    auth_db, users_collection, user_sessions_collection,
    patient_db, collection, patient_history_collection,
    audit_db, access_logs_collection, data_changes_collection
)
from app.db_manager import DatabaseManager
from werkzeug.security import generate_password_hash
from datetime import datetime


def setup_databases():
    """Initialize all three interconnected databases with proper structure."""
    
    print("="*60)
    print("Setting up Multiple Interconnected Databases")
    print("="*60)
    
    # Database 1: User Management Database
    print("\n1. Setting up USER MANAGEMENT DATABASE...")
    print("   Database: user_management_db")
    print("   Collections: users, sessions")
    
    # Create indexes for better performance
    users_collection.create_index("email", unique=True)
    user_sessions_collection.create_index("user_email")
    user_sessions_collection.create_index("session_id")
    
    # Check if admin exists
    admin_email = "admin@example.com"
    if not users_collection.find_one({'email': admin_email}):
        admin_user = {
            'email': admin_email,
            'password': generate_password_hash('AdminPass123'),
            'fullName': 'System Administrator',
            'role': 'admin',
            'created_at': datetime.utcnow()
        }
        users_collection.insert_one(admin_user)
        print(f"   ✓ Created admin user: {admin_email}")
        
        # Log admin creation to audit database (cross-database operation)
        DatabaseManager.log_data_change(
            user_email='system',
            operation='CREATE',
            database='user_management_db',
            collection_name='users',
            record_id=admin_email,
            new_data={'email': admin_email, 'fullName': 'System Administrator', 'role': 'admin'}
        )
    else:
        print(f"   ✓ Admin user already exists: {admin_email}")
    
    user_count = users_collection.count_documents({})
    session_count = user_sessions_collection.count_documents({})
    print(f"   ✓ Total users: {user_count}")
    print(f"   ✓ Total sessions: {session_count}")
    
    # Database 2: Patient Records Database
    print("\n2. Setting up PATIENT RECORDS DATABASE...")
    print("   Database: stroke_patient_db")
    print("   Collections: patients, patient_history")
    
    # Create indexes
    collection.create_index("id", unique=True)
    patient_history_collection.create_index("patient_id")
    patient_history_collection.create_index("modified_at")
    
    patient_count = collection.count_documents({})
    history_count = patient_history_collection.count_documents({})
    print(f"   ✓ Total patients: {patient_count}")
    print(f"   ✓ Total history records: {history_count}")
    
    # Database 3: Audit and Logging Database
    print("\n3. Setting up AUDIT & LOGGING DATABASE...")
    print("   Database: audit_logs_db")
    print("   Collections: access_logs, data_changes")
    
    # Create indexes for audit logs
    access_logs_collection.create_index("user_email")
    access_logs_collection.create_index("timestamp")
    data_changes_collection.create_index("user_email")
    data_changes_collection.create_index("record_id")
    data_changes_collection.create_index("timestamp")
    
    access_log_count = access_logs_collection.count_documents({})
    change_log_count = data_changes_collection.count_documents({})
    print(f"   ✓ Total access logs: {access_log_count}")
    print(f"   ✓ Total change logs: {change_log_count}")
    
    # Verify interconnections
    print("\n4. VERIFYING DATABASE INTERCONNECTIONS...")
    status = DatabaseManager.verify_database_connections()
    
    if status['status'] == 'success':
        print("   ✓ All three databases are interconnected and accessible")
        for db_name, db_status in status['databases'].items():
            print(f"   ✓ {db_name}: {db_status}")
    else:
        print(f"   ✗ Error: {status['message']}")
        return False
    
    # Demonstrate interconnection
    print("\n5. DEMONSTRATING CROSS-DATABASE OPERATIONS...")
    
    # Log a test access that spans databases
    DatabaseManager.log_access('system', 'database_setup', 'migration_script', 
                               {'databases_created': 3, 'collections_created': 6})
    print("   ✓ Created cross-database audit log")
    
    # Summary
    print("\n" + "="*60)
    print("DATABASE ARCHITECTURE SUMMARY")
    print("="*60)
    print(f"""
╔════════════════════════════════════════════════════════════╗
║  DATABASE 1: user_management_db                            ║
║  Purpose: User authentication and session management       ║
║  Collections:                                              ║
║    - users: {user_count} records                                          ║
║    - sessions: {session_count} records                                      ║
╠════════════════════════════════════════════════════════════╣
║  DATABASE 2: stroke_patient_db                             ║
║  Purpose: Patient medical records and history              ║
║  Collections:                                              ║
║    - patients: {patient_count} records                                  ║
║    - patient_history: {history_count} records                              ║
╠════════════════════════════════════════════════════════════╣
║  DATABASE 3: audit_logs_db                                 ║
║  Purpose: Security auditing and change tracking            ║
║  Collections:                                              ║
║    - access_logs: {access_log_count} records                                  ║
║    - data_changes: {change_log_count} records                                 ║
╠════════════════════════════════════════════════════════════╣
║  INTERCONNECTIONS:                                         ║
║  • Login: user_management_db → audit_logs_db               ║
║  • Patient Add: stroke_patient_db ← → audit_logs_db        ║
║  • Patient Update: stroke_patient_db → patient_history     ║
║                    → audit_logs_db                         ║
║  • Patient Delete: stroke_patient_db → audit_logs_db       ║
║  • Activity Report: All 3 databases queried together       ║
╚════════════════════════════════════════════════════════════╝
""")
    
    print("\n✓ Multiple interconnected databases setup complete!")
    print(f"✓ Admin credentials: {admin_email} / AdminPass123")
    print("\nTest the interconnection with these API endpoints:")
    print("  • /api/my-activity-report - Cross-database activity report")
    print("  • /api/patient/<id>/full-history - Patient history across databases")
    print("  • /api/database-status - Verify all database connections")
    
    return True


if __name__ == '__main__':
    try:
        success = setup_databases()
        if success:
            print("\n" + "="*60)
            print("Migration completed successfully!")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("Migration failed!")
            print("="*60)
    except Exception as e:
        print(f"\nError during migration: {e}")
        import traceback
        traceback.print_exc()
