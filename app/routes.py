from flask import Blueprint, redirect, render_template, request, jsonify, url_for, session
from app.config import collection, users_collection
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
import json  

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('index.html')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        print('login attempt')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Input validation
        if not email or not password:
            return render_template('login.html', error='Email and password are required')
        
        # Find user in database
        user = users_collection.find_one({'email': email})
        
        if user and check_password_hash(user['password'], password):
            # Store user info in session
            session['user'] = email
            session['fullName'] = user.get('fullName', 'User')
            print(f'Login successful: {email}')
            return redirect(url_for('dashboard.dashboard'))
        else:
            print('bad login')
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
@auth_bp.route('/register', methods=['GET', 'POST'])
def register(): 
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        fullName = request.form.get('fullName')
        role = request.form.get('role')
        
        # Input validation
        if not email or not password or not fullName:
            return render_template('register.html', error='All fields are required')
        
        if len(password) < 6:
            return render_template('register.html', error='Password must be at least 6 characters')
        
        # Check if user already exists
        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            return render_template('register.html', error='Email already registered')
        
        # Hash password and store user in database
        hashed_password = generate_password_hash(password)
        user_data = {
            'email': email,
            'password': hashed_password,
            'fullName': fullName,
            'role': role or 'user'
        }
        
        try:
            users_collection.insert_one(user_data)
            print(f'Registration successful: {email}, {fullName}, {role}')
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f'Registration error: {e}')
            return render_template('register.html', error='Registration failed. Please try again.')
    
    return render_template('register.html')

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

@dashboard_bp.route('/patient')
def get_data():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('patient.html')

@dashboard_bp.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'GET':
        return render_template('add_patient.html')
    
    if request.method == 'POST':
        try:
            # Get form data
            patient_data = {
                'id': int(request.form.get('id')),
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
            
            # Check if patient ID already exists
            existing = collection.find_one({'id': patient_data['id']})
            if existing:
                return jsonify({'success': False, 'message': 'Patient ID already exists'}), 400
            
            # Insert into MongoDB
            collection.insert_one(patient_data)
            
            return jsonify({'success': True, 'message': 'Patient added successfully'}), 200
            
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

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
        
        # Update in MongoDB
        result = collection.update_one({'id': patient_id}, {'$set': patient_data})
        
        if result.matched_count == 0:
            return jsonify({'success': False, 'message': 'Patient not found'}), 404
        
        return jsonify({'success': True, 'message': 'Patient updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@dashboard_bp.route('/api/patient/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete a patient record."""
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        result = collection.delete_one({'id': patient_id})
        
        if result.deleted_count == 0:
            return jsonify({'success': False, 'message': 'Patient not found'}), 404
        
        return jsonify({'success': True, 'message': 'Patient deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
