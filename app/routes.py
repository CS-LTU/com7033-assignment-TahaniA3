"""
Application Routes Module
==========================
This module defines all HTTP routes and request handlers for the Stroke Patient
Management System. It implements secure authentication, patient CRUD operations,
and RESTful API endpoints.

Blueprint Architecture:
    - auth_bp: Authentication routes (login, register, logout)
    - dashboard_bp: Patient management and dashboard routes

Security Features:
    - Rate limiting to prevent brute force attacks
    - CSRF protection on all forms (Flask-WTF)
    - Input sanitization to prevent XSS attacks
    - NoSQL injection prevention
    - Session-based authentication
    - Audit logging for all sensitive operations

Routes Overview:
    Authentication:
        GET/POST /login - User login
        GET/POST /register - User registration
        GET /logout - User logout
        
    Patient Management:
        GET /dashboard - Dashboard with statistics
        GET /patient - Patient list
        GET/POST /add_patient - Add new patient
        
    API Endpoints:
        GET /api/patients - Fetch all patients
        GET /api/dashboard-stats - Get statistics
        PUT /api/patient/<id> - Update patient
        DELETE /api/patient/<id> - Delete patient
        GET /api/my-activity-report - User activity log
        GET /api/database-status - Database health check

Author: Tahani A3
Course: COM7033 - Secure Software Development
"""

# ============================================================================
# Import Required Libraries
# ============================================================================
from flask import Blueprint, redirect, render_template, request, jsonify, url_for, session
from app.config import collection, users_collection
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
import json
from app.db_manager import DatabaseManager  # Cross-database operations
from app.security import SecurityUtils  # Input validation and sanitization
from app import limiter  # Rate limiting for attack prevention
import secrets  # Cryptographically secure random tokens

# ============================================================================
# Blueprint Registration
# ============================================================================
# Blueprints allow modular organization of routes
# auth_bp: Handles authentication-related routes
auth_bp = Blueprint('auth', __name__)

# ============================================================================
# Public Routes (No Authentication Required)
# ============================================================================

@auth_bp.route('/')
def home():
    """
    Home page route - Landing page for the application
    
    Returns:
        HTML: Renders index.html template with welcome message and login/register links
        
    Security: Public route, no authentication required
    """
    return render_template('index.html')
@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Rate limiting: prevent brute force attacks
def login():
    """Login with security: rate limiting, input sanitization, audit logging."""
    if request.method == 'POST':
        try:
            print('login attempt')
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            
            # Input validation and sanitization
            if not email or not password:
                return render_template('login.html', error='Email and password are required')
            
            # Validate and sanitize email (XSS prevention)
            email = SecurityUtils.validate_email(email)
            
            # Find user in user management database
            user = users_collection.find_one({'email': email})
            
            if user and check_password_hash(user['password'], password):
                # Store user info in session
                session['user'] = email
                session['fullName'] = SecurityUtils.sanitize_html(user.get('fullName', 'User'))
                
                # Generate cryptographically secure session ID
                session_id = secrets.token_urlsafe(32)
                session['session_id'] = session_id
                session.permanent = True  # Use permanent session with timeout
                
                # Log session in user management database and audit database
                DatabaseManager.create_user_session(email, session_id)
                
                print(f'Login successful: {email}')
                return redirect(url_for('dashboard.dashboard'))
            else:
                # Log failed login attempt to audit database
                DatabaseManager.log_access('anonymous', 'failed_login', 'system', 
                                          {'attempted_email': SecurityUtils.sanitize_html(email)})
                print('bad login')
                return render_template('login.html', error='Invalid email or password')
        
        except ValueError as e:
            # Catch validation errors
            return render_template('login.html', error=str(e))
        except Exception as e:
            print(f'Login error: {e}')
            return render_template('login.html', error='An error occurred during login')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Logout with session termination across databases."""
    user_email = session.get('user')
    session_id = session.get('session_id')
    
    # End session in user management database and log to audit database
    if user_email and session_id:
        DatabaseManager.end_user_session(user_email, session_id)
    
    session.clear()
    return redirect(url_for('auth.login'))
@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("3 per minute")  # Rate limiting: prevent spam registrations
def register():
    """Registration with input sanitization and validation."""
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            fullName = request.form.get('fullName', '').strip()
            role = request.form.get('role', 'user')
            
            # Input validation and sanitization
            if not email or not password or not fullName:
                return render_template('register.html', error='All fields are required')
            
            # Validate and sanitize inputs (XSS prevention)
            email = SecurityUtils.validate_email(email)
            fullName = SecurityUtils.sanitize_html(fullName)
            role = SecurityUtils.sanitize_html(role)
            
            # Validate password strength
            SecurityUtils.validate_password(password)
            
            if len(password) < 8:
                return render_template('register.html', error='Password must be at least 8 characters')
            
            # Check if user already exists (prevent timing attacks by always checking)
            existing_user = users_collection.find_one({'email': email})
            if existing_user:
                return render_template('register.html', error='Email already registered')
            
            # Hash password with strong algorithm (PBKDF2-SHA256)
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
            user_data = {
                'email': email,
                'password': hashed_password,
                'fullName': fullName,
                'role': role if role in ['user', 'admin'] else 'user'  # Role validation
            }
            
            # Insert into user management database
            users_collection.insert_one(user_data)
            
            # Log registration to audit database (interconnected operation)
            DatabaseManager.log_data_change(
                user_email='system',
                operation='CREATE',
                database='user_management_db',
                collection_name='users',
                record_id=email,
                new_data={'email': email, 'fullName': fullName, 'role': user_data['role']}
            )
            
            print(f'Registration successful: {email}, {fullName}, {role}')
            return redirect(url_for('auth.login'))
            
        except ValueError as e:
            # Catch validation errors
            return render_template('register.html', error=str(e))
        except Exception as e:
            print(f'Registration error: {e}')
            return render_template('register.html', error='Registration failed. Please try again.')
    
    return render_template('register.html')

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    """Dashboard with audit logging across databases."""
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    # Log dashboard access to audit database
    DatabaseManager.log_access(session['user'], 'view_dashboard', 'dashboard')
    
    return render_template('dashboard.html')

@dashboard_bp.route('/patient')
def get_data():
    """Patient list with audit logging."""
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    # Log patient list access to audit database
    DatabaseManager.log_access(session['user'], 'view_patient_list', 'patient_page')
    
    return render_template('patient.html')

@dashboard_bp.route('/add_patient', methods=['GET', 'POST'])
@limiter.limit("10 per minute")  # Rate limiting
def add_patient():
    """Add patient with input sanitization and validation."""
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'GET':
        return render_template('add_patient.html')
    
    if request.method == 'POST':
        try:
            # Get and validate patient data with comprehensive security checks
            patient_data = SecurityUtils.validate_patient_data(request.form.to_dict())
            
            # Check if patient ID already exists in patient database
            existing = collection.find_one({'id': patient_data['id']})
            if existing:
                return jsonify({'success': False, 'message': 'Patient ID already exists'}), 400
            
            # Insert patient using interconnected database manager
            # This inserts to patient database AND logs to audit database
            DatabaseManager.add_patient_with_audit(session['user'], patient_data)
            
            return jsonify({'success': True, 'message': 'Patient added successfully'}), 200
            
        except ValueError as e:
            # Validation errors
            return jsonify({'success': False, 'message': f'Validation error: {str(e)}'}), 400
        except Exception as e:
            print(f'Add patient error: {e}')
            return jsonify({'success': False, 'message': 'Failed to add patient'}), 500

@dashboard_bp.route('/api/patients')
def api_patients():
    """Fetch all patient records from MongoDB."""
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Exclude the 'columns' field and MongoDB _id from response
        patients = list(collection.find({}, {'_id': 0, 'columns': 0}))
        # Use json_util to handle any special BSON types
        return json.loads(json_util.dumps(patients)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/api/dashboard-stats')
def api_dashboard_stats():
    """Calculate aggregate statistics from MongoDB for dashboard."""
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        total_patients = collection.count_documents({})
        stroke_cases = collection.count_documents({'stroke': 1})
        high_risk = collection.count_documents({
            '$or': [
                {'hypertension': 1, 'heart_disease': 1},
                {'age': {'$gte': 65}, 'hypertension': 1}
            ]
        })
        
        # Calculate average age
        pipeline = [
            {'$group': {'_id': None, 'avgAge': {'$avg': '$age'}}}
        ]
        avg_result = list(collection.aggregate(pipeline))
        avg_age = avg_result[0]['avgAge'] if avg_result else 0
        
        # Gender distribution
        gender_pipeline = [
            {'$group': {'_id': '$gender', 'count': {'$sum': 1}}}
        ]
        gender_dist = list(collection.aggregate(gender_pipeline))
        
        stats = {
            'totalPatients': total_patients,
            'strokeCases': stroke_cases,
            'highRisk': high_risk,
            'avgAge': round(avg_age, 1),
            'genderDistribution': {item['_id']: item['count'] for item in gender_dist}
        }
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/api/patient/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update an existing patient record."""
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Get form data
        patient_data = {
            'age': int(request.form.get('age')) if request.form.get('age') else None,
            'gender': request.form.get('gender'),
            'hypertension': int(request.form.get('hypertension')) if request.form.get('hypertension') else 0,
            'heart_disease': int(request.form.get('heart_disease')) if request.form.get('heart_disease') else 0,
            'ever_married': request.form.get('ever_married'),
            'work_type': request.form.get('work_type'),
            'Residence_type': request.form.get('Residence_type'),
            'avg_glucose_level': float(request.form.get('avg_glucose_level')) if request.form.get('avg_glucose_level') else None,
            'bmi': float(request.form.get('bmi')) if request.form.get('bmi') else None,
            'smoking_status': request.form.get('smoking_status'),
            'stroke': int(request.form.get('stroke')) if request.form.get('stroke') else 0
        }
        
        # Get old data before update (for audit history)
        old_data = collection.find_one({'id': patient_id})
        
        if not old_data:
            return jsonify({'success': False, 'message': 'Patient not found'}), 404
        
        # Update using interconnected database manager
        # This updates patient database, saves history, and logs to audit database
        DatabaseManager.update_patient_with_history(
            session['user'], patient_id, old_data, patient_data
        )
        
        return jsonify({'success': True, 'message': 'Patient updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@dashboard_bp.route('/api/patient/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete a patient record."""
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Delete using interconnected database manager
        # This deletes from patient database AND logs to audit database
        result = DatabaseManager.delete_patient_with_audit(session['user'], patient_id)
        
        if not result or result.deleted_count == 0:
            return jsonify({'success': False, 'message': 'Patient not found'}), 404
        
        return jsonify({'success': True, 'message': 'Patient deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ============================================
# Interconnected Database Demonstration Routes
# ============================================

@dashboard_bp.route('/api/my-activity-report')
def my_activity_report():
    """
    Generate cross-database activity report.
    Demonstrates interconnection between user_management_db, stroke_patient_db, and audit_logs_db.
    """
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Get comprehensive report from all three databases
        report = DatabaseManager.get_user_activity_report(session['user'])
        
        # Convert MongoDB objects to JSON-serializable format
        report_json = json.loads(json_util.dumps(report))
        
        return jsonify({
            'success': True,
            'report': report_json,
            'message': 'Data retrieved from multiple interconnected databases'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/api/patient/<int:patient_id>/full-history')
def patient_full_history(patient_id):
    """
    Get complete patient history across databases.
    Retrieves data from stroke_patient_db (current + history) and audit_logs_db.
    """
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Log access to audit database
        DatabaseManager.log_access(session['user'], 'view_patient_history', f'patient_id:{patient_id}')
        
        # Get history from multiple databases
        history = DatabaseManager.get_patient_full_history(patient_id)
        
        # Convert to JSON
        history_json = json.loads(json_util.dumps(history))
        
        return jsonify({
            'success': True,
            'history': history_json,
            'message': 'Complete history from patient and audit databases'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/api/database-status')
def database_status():
    """
    Verify connectivity to all three interconnected databases.
    """
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        status = DatabaseManager.verify_database_connections()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
