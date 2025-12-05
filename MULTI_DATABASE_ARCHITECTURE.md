# Multiple Interconnected Databases Architecture

## Overview
This application utilizes **three separate MongoDB databases** that are interconnected to enable secure data management and efficient data retrieval across different functional domains.

## Database Architecture

### 🗄️ Database 1: **user_management_db**
**Purpose:** User authentication, profiles, and session management

**Collections:**
- **`users`** - Stores user credentials and profiles
  - Fields: email, password (hashed), fullName, role, created_at
  - Indexes: email (unique)
  
- **`sessions`** - Tracks active user sessions
  - Fields: user_email, session_id, login_time, last_activity, logout_time, active
  - Indexes: user_email, session_id
  - **Interconnection:** Links to users collection via user_email

### 🏥 Database 2: **stroke_patient_db**
**Purpose:** Medical records and patient data management

**Collections:**
- **`patients`** - Main patient medical records
  - Fields: id, age, gender, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status, stroke
  - Indexes: id (unique)
  
- **`patient_history`** - Historical changes to patient records
  - Fields: patient_id, modified_by, modified_at, old_data, new_data
  - Indexes: patient_id, modified_at
  - **Interconnection:** Links to patients collection via patient_id AND links to user_management_db via modified_by (user email)

### 📝 Database 3: **audit_logs_db**
**Purpose:** Security auditing, compliance, and activity tracking

**Collections:**
- **`access_logs`** - Records all system access events
  - Fields: user_email, action, resource, timestamp, details
  - Indexes: user_email, timestamp
  - **Interconnection:** Links to user_management_db via user_email
  
- **`data_changes`** - Tracks all CRUD operations
  - Fields: user_email, operation, database, collection, record_id, old_data, new_data, timestamp
  - Indexes: user_email, record_id, timestamp
  - **Interconnections:** 
    - Links to user_management_db via user_email
    - References patient_db via record_id
    - Tracks changes across all databases

## Interconnection Flow

### 1. User Login Flow
```
user_management_db (users) 
    ↓ authenticate
user_management_db (sessions) ← create session
    ↓ log event
audit_logs_db (access_logs) ← record login
```

### 2. Patient Creation Flow
```
stroke_patient_db (patients) ← insert patient
    ↓ record action
audit_logs_db (data_changes) ← log creation
    ↓ track access
audit_logs_db (access_logs) ← log user access
```

### 3. Patient Update Flow
```
stroke_patient_db (patients) ← get old data
    ↓ update record
stroke_patient_db (patients) ← save new data
    ↓ save history
stroke_patient_db (patient_history) ← store change
    ↓ audit trail
audit_logs_db (data_changes) ← log modification
    ↓ access log
audit_logs_db (access_logs) ← record activity
```

### 4. Patient Delete Flow
```
stroke_patient_db (patients) ← get data
    ↓ delete record
stroke_patient_db (patients) ← remove
    ↓ audit
audit_logs_db (data_changes) ← log deletion
    ↓ track
audit_logs_db (access_logs) ← record access
```

### 5. Cross-Database Activity Report
```
user_management_db (users) ← get user info
user_management_db (sessions) ← get sessions
audit_logs_db (access_logs) ← get activity
audit_logs_db (data_changes) ← get modifications
    ↓ combine
Complete User Activity Report
```

## Database Manager (app/db_manager.py)

The `DatabaseManager` class orchestrates operations across all three databases:

### Key Methods:

**Session Management:**
- `create_user_session()` - Creates session in user_management_db, logs to audit_logs_db
- `end_user_session()` - Ends session in user_management_db, logs to audit_logs_db

**Patient Operations:**
- `add_patient_with_audit()` - Inserts to patient_db, logs to audit_db
- `update_patient_with_history()` - Updates patient_db, saves history, logs to audit_db
- `delete_patient_with_audit()` - Deletes from patient_db, logs to audit_db

**Access Logging:**
- `log_access()` - Records user actions to audit_db
- `log_data_change()` - Tracks data modifications to audit_db

**Cross-Database Queries:**
- `get_user_activity_report()` - Queries all 3 databases for comprehensive user report
- `get_patient_full_history()` - Retrieves patient data from patient_db and audit_db
- `verify_database_connections()` - Tests connectivity to all databases

## API Endpoints Demonstrating Interconnection

### Standard Endpoints (with audit logging):
- `POST /login` - Touches: user_management_db + audit_logs_db
- `POST /register` - Touches: user_management_db + audit_logs_db
- `GET /logout` - Touches: user_management_db + audit_logs_db
- `GET /dashboard` - Touches: audit_logs_db (logs access)
- `GET /patient` - Touches: stroke_patient_db + audit_logs_db
- `POST /add_patient` - Touches: stroke_patient_db + audit_logs_db
- `PUT /api/patient/<id>` - Touches: stroke_patient_db (patients + history) + audit_logs_db
- `DELETE /api/patient/<id>` - Touches: stroke_patient_db + audit_logs_db

### Cross-Database Report Endpoints:
- `GET /api/my-activity-report` - Queries all 3 databases simultaneously
- `GET /api/patient/<id>/full-history` - Queries stroke_patient_db + audit_logs_db
- `GET /api/database-status` - Verifies connectivity to all 3 databases

## Setup Instructions

### 1. Run the database setup script:
```powershell
python scripts/setup_multi_databases.py
```

This will:
- Create all 3 databases with proper structure
- Set up indexes for efficient queries
- Create initial admin user
- Verify interconnections
- Display architecture summary

### 2. Load patient data:
```powershell
python scripts/load_csv_to_mongo.py
```

### 3. Start the application:
```powershell
python run.py
```

## Security Benefits of Multiple Databases

1. **Data Segregation:** User credentials, patient data, and audit logs are physically separated
2. **Access Control:** Different databases can have different permission levels
3. **Audit Trail:** Complete audit database tracks all actions across other databases
4. **Data Integrity:** Patient history preserved even if current data is deleted
5. **Compliance:** Separate audit database meets regulatory requirements
6. **Scalability:** Individual databases can be scaled independently

## Verification

To verify the interconnected database architecture:

1. **Check database status:**
   ```
   GET /api/database-status
   ```
   Should show all 3 databases as "connected"

2. **Perform an action and check cross-database logging:**
   - Add a patient (touches patient_db + audit_db)
   - View activity report (queries all 3 databases)
   
3. **View patient history:**
   ```
   GET /api/patient/<id>/full-history
   ```
   Shows data from patient_db (current + history) + audit_db

## Database Statistics

After setup:
- **user_management_db:** 1 admin user, 0 sessions initially
- **stroke_patient_db:** 5,110 patient records, 0 history records initially
- **audit_logs_db:** Logs created during setup

## Conclusion

This architecture demonstrates:
- ✅ **Multiple databases:** 3 separate MongoDB databases
- ✅ **Interconnected:** Data relationships and cross-database queries
- ✅ **Secure management:** Password hashing, session tracking, audit logging
- ✅ **Efficient retrieval:** Indexed collections, optimized queries, cross-database reports
