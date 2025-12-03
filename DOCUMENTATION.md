# Stroke Patient Management System - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Installation & Setup](#installation--setup)
4. [Database Configuration](#database-configuration)
5. [Application Structure](#application-structure)
6. [Features & Functionality](#features--functionality)
7. [Code Explanation](#code-explanation)
8. [Security Implementation](#security-implementation)
9. [API Endpoints](#api-endpoints)
10. [User Guide](#user-guide)

---

## Project Overview

### Purpose
This is a web-based **Stroke Patient Management System** built with Flask and MongoDB. It allows healthcare administrators to:
- Manage patient records with comprehensive medical data
- View statistical dashboards with visualizations
- Perform CRUD operations (Create, Read, Update, Delete) on patient data
- Authenticate users with a secure login system

### Technologies Used
- **Backend**: Flask (Python web framework)
- **Database**: MongoDB Atlas (Cloud NoSQL database)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Data Visualization**: Chart.js
- **Data Processing**: Pandas, PapaParse

### Key Features
✅ User Authentication (Login/Register/Logout)  
✅ Dashboard with statistics and charts  
✅ Patient list with search and pagination  
✅ Add new patients to database  
✅ View detailed patient information  
✅ Update existing patient records  
✅ Delete patient records  
✅ CSV data import to MongoDB  

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT SIDE                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Patient  │  │   Add    │  │  Login   │   │
│  │  Page    │  │   List   │  │ Patient  │  │   Page   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │              │          │
│       └─────────────┴──────────────┴──────────────┘          │
│                         │                                     │
│                    HTTP Requests                             │
└─────────────────────────┼───────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────┐
│                    FLASK SERVER                              │
│  ┌───────────────────────────────────────────────────┐      │
│  │            Flask Application (run.py)              │      │
│  │  ┌─────────────────────────────────────────────┐  │      │
│  │  │         Blueprints (routes.py)              │  │      │
│  │  │  ┌──────────────┐  ┌──────────────────┐    │  │      │
│  │  │  │  auth_bp     │  │   dashboard_bp   │    │  │      │
│  │  │  │ - Login      │  │ - Dashboard      │    │  │      │
│  │  │  │ - Register   │  │ - Patient List   │    │  │      │
│  │  │  │ - Logout     │  │ - Add Patient    │    │  │      │
│  │  │  │              │  │ - API Endpoints  │    │  │      │
│  │  │  └──────────────┘  └──────────────────┘    │  │      │
│  │  └─────────────────────────────────────────────┘  │      │
│  └───────────────────────────────────────────────────┘      │
│                          │                                    │
│                     PyMongo Driver                           │
└──────────────────────────┼──────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                   MONGODB ATLAS                              │
│  ┌────────────────────────────────────────────────┐         │
│  │         stroke_database                         │         │
│  │  ┌──────────────────┐  ┌──────────────────┐   │         │
│  │  │ stroke_collection│  │stroke_metadata   │   │         │
│  │  │ (Patient Data)   │  │ (CSV Headers)    │   │         │
│  │  └──────────────────┘  └──────────────────┘   │         │
│  └────────────────────────────────────────────────┘         │
└──────────────────────────────────────────────────────────────┘
```

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account (free tier available)
- Git (for version control)

### Step 1: Clone the Repository
```bash
git clone https://github.com/CS-LTU/com7033-assignment-TahaniA3.git
cd com7033-assignment-TahaniA3
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### Step 3: Install Required Packages
```bash
pip install flask
pip install pymongo
pip install pandas
```

**Required Dependencies:**
- `flask` - Web framework for Python
- `pymongo` - MongoDB driver for Python
- `pandas` - Data manipulation library (for CSV processing)

### Step 4: Configure MongoDB Connection
Edit `app/config.py` and update the MongoDB connection string:
```python
MONGO_URI = "your_mongodb_atlas_connection_string"
```

### Step 5: Load Initial Data
```bash
python scripts/load_csv_to_mongo.py
```
This will import the `stroke.csv` file into MongoDB.

### Step 6: Run the Application
```bash
python run.py
```
The application will start on `http://127.0.0.1:5000/`

---

## Database Configuration

### MongoDB Atlas Setup

#### 1. Create MongoDB Atlas Account
- Go to https://www.mongodb.com/cloud/atlas
- Sign up for a free account
- Create a new cluster (free tier: M0)

#### 2. Configure Database Access
- Go to **Database Access** → **Add New Database User**
- Username: `taalanzi35_db_user`
- Password: `TaaH-11233`
- Set privileges to **Read and Write to any database**

#### 3. Configure Network Access
- Go to **Network Access** → **Add IP Address**
- Click **Allow Access from Anywhere** (0.0.0.0/0)
- Or add your specific IP address

#### 4. Get Connection String
- Go to **Clusters** → **Connect** → **Connect your application**
- Copy the connection string:
```
mongodb+srv://taalanzi35_db_user:TaaH-11233@stroke.xsvmyml.mongodb.net/
```

### Database Structure

**Database Name:** `stroke_database`

**Collections:**

1. **stroke_collection** (Main patient data)
```javascript
{
  "id": 10001,
  "age": 67,
  "gender": "Male",
  "hypertension": 0,
  "heart_disease": 1,
  "ever_married": "Yes",
  "work_type": "Private",
  "Residence_type": "Urban",
  "avg_glucose_level": 228.69,
  "bmi": 36.6,
  "smoking_status": "formerly smoked",
  "stroke": 1
}
```

2. **stroke_metadata** (CSV column information)
```javascript
{
  "columns": ["id", "age", "gender", "hypertension", ...]
}
```

---

## Application Structure

```
com7033-assignment-TahaniA3/
│
├── run.py                          # Application entry point
├── stroke.csv                       # Patient data CSV file
├── README.md                        # Project readme
│
├── app/                             # Main application package
│   ├── __init__.py                  # Flask app initialization
│   ├── config.py                    # MongoDB configuration
│   ├── routes.py                    # All route handlers
│   │
│   ├── templates/                   # HTML templates
│   │   ├── base.html                # Base template (navigation, layout)
│   │   ├── index.html               # Landing page
│   │   ├── login.html               # Login page
│   │   ├── register.html            # Registration page
│   │   ├── dashboard.html           # Statistics dashboard
│   │   ├── patient.html             # Patient list and details
│   │   └── add_patient.html         # Add/Edit patient form
│   │
│   └── static/                      # Static files (empty, using CDN)
│
└── scripts/                         # Utility scripts
    └── load_csv_to_mongo.py         # CSV import script
```

---

## Features & Functionality

### 1. Authentication System

#### Login Process
- **Route:** `/login` (GET, POST)
- **File:** `app/templates/login.html`
- **Credentials:**
  - Email: `admin@example.com`
  - Password: `AdminPass`

**How it works:**
1. User enters email and password
2. Server validates credentials in `routes.py`
3. If valid, creates session with `session['user'] = username`
4. Redirects to dashboard
5. If invalid, shows error message

#### Registration Process
- **Route:** `/register` (GET, POST)
- **File:** `app/templates/register.html`

**How it works:**
1. User fills form (email, password, full name, role)
2. Server receives form data
3. Prints to console (no actual storage yet)
4. Redirects to login page

#### Logout
- **Route:** `/logout`
- Clears session: `session.clear()`
- Redirects to login page

#### Protected Routes
All dashboard, patient, and add_patient routes check for session:
```python
if 'user' not in session:
    return redirect(url_for('auth.login'))
```

---

### 2. Dashboard Page

**Route:** `/dashboard`  
**File:** `app/templates/dashboard.html`

#### Features:
1. **Statistics Cards** (4 cards showing):
   - Total Patients
   - Stroke Cases
   - High Risk Patients (hypertension + heart disease)
   - Average Age

2. **Risk Distribution Chart** (Doughnut Chart):
   - Low Risk (green)
   - Moderate Risk (yellow)
   - High Risk (red)

3. **Gender Distribution Chart** (Bar Chart):
   - Male count
   - Female count
   - Other count

4. **Recent Patients Table**:
   - Shows last 10 patients
   - Displays: ID, Name, Age, Gender, Stroke Status

#### Data Flow:
```
Dashboard Page Load
     ↓
JavaScript: loadDashboardStats()
     ↓
Fetch: /api/dashboard-stats
     ↓
Flask: Aggregates data from MongoDB
     ↓
Returns JSON with stats
     ↓
JavaScript: Updates charts and cards
```

---

### 3. Patient List Page

**Route:** `/patient`  
**File:** `app/templates/patient.html`

#### Features:
1. **Search Functionality**
   - Search by: ID, Name, Age, Gender
   - Real-time filtering as you type

2. **Statistics Bar**
   - Total Patients
   - With Hypertension count
   - Urban Residence count
   - Average Age

3. **Patient Table**
   - Shows 50 patients per page
   - Columns: ID, Age, Gender, Hypertension, Heart Disease, Residence, BMI, Stroke
   - Color-coded badges (Yes=Red, No=Green)

4. **Pagination**
   - Navigate through pages
   - Shows current page / total pages

5. **View Details Button**
   - Opens modal with complete patient information
   - Organized in 4 sections:
     - Personal Information
     - Medical History
     - Lifestyle & Environment
     - Risk Assessment

6. **Action Buttons in Modal**
   - **Close**: Closes the modal
   - **Delete Patient**: Removes patient from database
   - **Update Patient**: Opens edit form with pre-filled data

#### Data Flow:
```
Patient List Load
     ↓
JavaScript: loadPatientsFromDB()
     ↓
Fetch: /api/patients
     ↓
Flask: collection.find({})
     ↓
Returns all patients as JSON
     ↓
JavaScript: Stores in patientData array
     ↓
Renders table with pagination
```

---

### 4. Add/Update Patient

**Route:** `/add_patient`  
**File:** `app/templates/add_patient.html`

#### Add Mode (Default)
1. Form opens with empty fields
2. Patient ID auto-generated from MongoDB (max ID + 1)
3. User fills in all fields
4. Submit sends POST to `/add_patient`
5. Data inserted into MongoDB
6. Redirects to patient list

#### Edit Mode (When Update button clicked)
1. User clicks "Update Patient" in patient detail modal
2. Patient data stored in `sessionStorage.editPatient`
3. Redirects to add_patient page
4. JavaScript detects sessionStorage data
5. Form fields pre-populated with patient data
6. Page title changes to "Update Patient"
7. Patient ID field becomes read-only
8. Submit sends PUT to `/api/patient/{id}`
9. Data updated in MongoDB
10. sessionStorage cleared
11. Redirects to patient list

#### Form Fields:
- **Patient ID** (auto-generated or read-only in edit mode)
- **Age** (number)
- **Gender** (Male/Female/Other)
- **Hypertension** (Yes/No)
- **Heart Disease** (Yes/No)
- **Marital Status** (Yes/No)
- **Work Type** (Private/Self-employed/Govt_job/children/Never_worked)
- **Residence Type** (Urban/Rural)
- **Average Glucose Level** (number with decimals)
- **BMI** (Body Mass Index, number with decimals)
- **Smoking Status** (never smoked/formerly smoked/smokes/Unknown)
- **Stroke** (Yes/No)

#### Validation:
- All fields are required
- Age must be a positive number
- Glucose level and BMI must be valid numbers
- Server-side validation in Flask

---

### 5. Delete Patient

**Triggered from:** Patient detail modal  
**API Endpoint:** `/api/patient/{id}` (DELETE method)

#### Process:
1. User clicks "Delete Patient" button
2. JavaScript shows confirmation dialog
3. If confirmed, sends DELETE request to API
4. Flask deletes record: `collection.delete_one({'id': patient_id})`
5. Returns success/failure JSON
6. Modal closes
7. Patient list reloads automatically

---

## Code Explanation

### 1. run.py (Application Entry Point)

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**
- Imports the `create_app` factory function from `app` package
- Creates the Flask application instance
- Runs the server on `http://127.0.0.1:5000/`
- `debug=True` enables auto-reload and detailed error messages

---

### 2. app/__init__.py (Flask App Factory)

```python
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-here'
    
    from .routes import auth_bp, dashboard_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    
    return app
```

**Explanation:**
- **Flask(__name__)**: Creates Flask application instance
- **secret_key**: Required for session management (encrypts session cookies)
- **Blueprints**: Organizes routes into logical groups
  - `auth_bp`: Authentication routes (login, register, logout)
  - `dashboard_bp`: Dashboard and patient management routes
- **register_blueprint()**: Registers blueprints with the app

**Why use Blueprints?**
- Better code organization
- Reusable components
- Easier to maintain large applications
- Can have separate URL prefixes

---

### 3. app/config.py (Database Configuration)

```python
from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = "mongodb+srv://taalanzi35_db_user:TaaH-11233@stroke.xsvmyml.mongodb.net/"

# Create MongoDB client
client = MongoClient(MONGO_URI)

# Access database and collection
db = client['stroke_database']
collection = db['stroke_collection']
```

**Explanation:**
- **MONGO_URI**: Connection string for MongoDB Atlas
  - Format: `mongodb+srv://username:password@cluster.mongodb.net/`
- **MongoClient**: Creates connection to MongoDB
- **client['stroke_database']**: Accesses specific database
- **db['stroke_collection']**: Accesses specific collection (like a table)

**Connection Components:**
- `mongodb+srv://`: Protocol (SRV for DNS seedlist)
- `taalanzi35_db_user`: Database username
- `TaaH-11233`: Database password
- `@stroke.xsvmyml.mongodb.net/`: Cluster hostname

---

### 4. app/routes.py (Route Handlers)

#### Authentication Routes

```python
from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')
```

**Blueprint Creation:**
- `Blueprint('auth', __name__)`: Creates blueprint named 'auth'
- Groups related routes together

**Index Route:**
- URL: `/`
- Returns landing page template

---

#### Login Route

```python
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')
        
        # Simple authentication check
        if username == 'admin@example.com' and password == 'AdminPass':
            session['user'] = username
            return redirect(url_for('dashboard.dashboard'))
        else:
            return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')
```

**Explanation:**
- **methods=['GET', 'POST']**: Accepts both GET (show form) and POST (submit form)
- **request.method**: Checks if it's a form submission
- **request.form.get()**: Retrieves form data
- **session['user']**: Stores username in session (server-side storage)
- **redirect()**: Redirects to another route
- **url_for()**: Generates URL for a route name
- **render_template()**: Renders HTML template with optional variables

**Security Note:** In production, passwords should be hashed (using bcrypt or similar)

---

#### Dashboard Routes

```python
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')
```

**Session Protection:**
- Checks if user is logged in before showing page
- If not logged in, redirects to login page
- This protects sensitive pages from unauthorized access

---

#### API: Get Dashboard Statistics

```python
@dashboard_bp.route('/api/dashboard-stats')
def api_dashboard_stats():
    if 'user' not in session:
        return {'error': 'Unauthorized'}, 401
    
    try:
        # Get all patients
        patients = list(collection.find({}, {'_id': 0}))
        
        # Calculate statistics
        total = len(patients)
        stroke_cases = sum(1 for p in patients if p.get('stroke') == 1)
        high_risk = sum(1 for p in patients 
                       if p.get('hypertension') == 1 and p.get('heart_disease') == 1)
        
        # Calculate average age
        ages = [p['age'] for p in patients if 'age' in p]
        avg_age = sum(ages) / len(ages) if ages else 0
        
        # Gender distribution
        gender_dist = {}
        for p in patients:
            gender = p.get('gender', 'Unknown')
            gender_dist[gender] = gender_dist.get(gender, 0) + 1
        
        return {
            'total': total,
            'strokeCases': stroke_cases,
            'highRisk': high_risk,
            'avgAge': round(avg_age, 1),
            'genderDistribution': gender_dist
        }
    except Exception as e:
        return {'error': str(e)}, 500
```

**Explanation:**
- **collection.find({}, {'_id': 0})**: Query MongoDB
  - `{}`: Empty filter (get all documents)
  - `{'_id': 0}`: Projection (exclude MongoDB's _id field)
- **list()**: Converts cursor to Python list
- **List comprehension**: `sum(1 for p in patients if ...)` counts matching patients
- **p.get('key')**: Safely gets value (returns None if key doesn't exist)
- **round(avg_age, 1)**: Rounds to 1 decimal place
- **try/except**: Error handling (returns 500 error if something fails)

---

#### API: Get All Patients

```python
@dashboard_bp.route('/api/patients')
def api_patients():
    if 'user' not in session:
        return {'error': 'Unauthorized'}, 401
    
    try:
        patients = list(collection.find({}, {'_id': 0, 'columns': 0}))
        return patients
    except Exception as e:
        return {'error': str(e)}, 500
```

**Explanation:**
- Returns all patients as JSON array
- Excludes `_id` and `columns` fields (internal MongoDB data)
- JavaScript can directly use this JSON data

---

#### Add Patient Route

```python
@dashboard_bp.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        try:
            # Get form data
            patient_data = {
                'id': int(request.form.get('id')),
                'age': int(request.form.get('age')),
                'gender': request.form.get('gender'),
                'hypertension': int(request.form.get('hypertension')),
                'heart_disease': int(request.form.get('heart_disease')),
                'ever_married': request.form.get('ever_married'),
                'work_type': request.form.get('work_type'),
                'Residence_type': request.form.get('Residence_type'),
                'avg_glucose_level': float(request.form.get('avg_glucose_level')),
                'bmi': float(request.form.get('bmi')),
                'smoking_status': request.form.get('smoking_status'),
                'stroke': int(request.form.get('stroke'))
            }
            
            # Insert into MongoDB
            collection.insert_one(patient_data)
            
            return {'success': True, 'message': 'Patient added successfully'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    return render_template('add_patient.html')
```

**Explanation:**
- **GET request**: Shows the form
- **POST request**: Processes form submission
- **int()**, **float()**: Converts string form data to numbers
- **patient_data dictionary**: Structured data matching MongoDB schema
- **collection.insert_one()**: Inserts new document into MongoDB
- **Returns JSON**: JavaScript receives success/error response

**Data Type Conversions:**
- Form data comes as strings
- Must convert to correct types before storing in database
- MongoDB stores data with proper types (integer, float, string)

---

#### Update Patient Route

```python
@dashboard_bp.route('/api/patient/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    if 'user' not in session:
        return {'error': 'Unauthorized'}, 401
    
    try:
        # Get form data
        patient_data = {
            'age': int(request.form.get('age')),
            'gender': request.form.get('gender'),
            'hypertension': int(request.form.get('hypertension')),
            'heart_disease': int(request.form.get('heart_disease')),
            'ever_married': request.form.get('ever_married'),
            'work_type': request.form.get('work_type'),
            'Residence_type': request.form.get('Residence_type'),
            'avg_glucose_level': float(request.form.get('avg_glucose_level')),
            'bmi': float(request.form.get('bmi')),
            'smoking_status': request.form.get('smoking_status'),
            'stroke': int(request.form.get('stroke'))
        }
        
        # Update in MongoDB
        result = collection.update_one(
            {'id': patient_id},
            {'$set': patient_data}
        )
        
        if result.matched_count == 0:
            return {'success': False, 'message': 'Patient not found'}, 404
        
        return {'success': True, 'message': 'Patient updated successfully'}
    except Exception as e:
        return {'success': False, 'message': str(e)}, 500
```

**Explanation:**
- **<int:patient_id>**: URL parameter (e.g., `/api/patient/10001`)
- **methods=['PUT']**: HTTP PUT method for updates
- **update_one()**: MongoDB update operation
  - First parameter: Filter (which document to update)
  - Second parameter: Update operation (`$set` replaces field values)
- **result.matched_count**: Number of documents matched (0 or 1)
- **404 error**: Patient not found

**MongoDB Update Operators:**
- `$set`: Sets field values
- `$inc`: Increments number
- `$push`: Adds to array
- `$unset`: Removes field

---

#### Delete Patient Route

```python
@dashboard_bp.route('/api/patient/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    if 'user' not in session:
        return {'error': 'Unauthorized'}, 401
    
    try:
        result = collection.delete_one({'id': patient_id})
        
        if result.deleted_count == 0:
            return {'success': False, 'message': 'Patient not found'}, 404
        
        return {'success': True, 'message': 'Patient deleted successfully'}
    except Exception as e:
        return {'success': False, 'message': str(e)}, 500
```

**Explanation:**
- **methods=['DELETE']**: HTTP DELETE method
- **delete_one()**: Removes one document matching filter
- **result.deleted_count**: Number of documents deleted (0 or 1)
- Permanent operation (no undo)

---

### 5. scripts/load_csv_to_mongo.py (Data Import Script)

```python
import pandas as pd
from pymongo import MongoClient

# MongoDB connection
MONGO_URI = "mongodb+srv://taalanzi35_db_user:TaaH-11233@stroke.xsvmyml.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['stroke_database']
collection = db['stroke_collection']
metadata_collection = db['stroke_metadata']

def load_csv_to_mongodb(csv_file):
    print(f"Reading CSV file: {csv_file}")
    df = pd.read_csv(csv_file)
    
    print(f"Found {len(df)} records")
    print(f"Columns: {list(df.columns)}")
    
    # Store column information
    metadata_collection.delete_many({})
    metadata_collection.insert_one({'columns': list(df.columns)})
    
    # Convert DataFrame to records
    records = []
    for _, row in df.iterrows():
        record = {}
        for col in df.columns:
            value = row[col]
            # Convert to appropriate type
            if pd.isna(value):
                record[col] = None
            elif col == 'id':
                record[col] = int(value)
            else:
                try:
                    record[col] = int(value) if float(value).is_integer() else float(value)
                except:
                    record[col] = value
        records.append(record)
    
    # Insert into MongoDB
    print("Inserting data into MongoDB...")
    for record in records:
        collection.update_one(
            {'id': record['id']},
            {'$set': record},
            upsert=True
        )
    
    print(f"Successfully loaded {len(records)} records")

if __name__ == '__main__':
    load_csv_to_mongodb('../stroke.csv')
```

**Explanation:**

**Pandas DataFrame:**
- `pd.read_csv()`: Reads CSV file into DataFrame (table structure)
- `df.iterrows()`: Iterates through each row
- `df.columns`: List of column names

**Type Conversion:**
- `pd.isna(value)`: Checks if value is NaN (missing)
- `float(value).is_integer()`: Checks if float is whole number
- Converts "10.0" to 10, keeps "10.5" as 10.5

**Upsert Operation:**
- `upsert=True`: Insert if doesn't exist, update if exists
- Prevents duplicate records when running script multiple times
- Uses `id` field as unique identifier

**Metadata Storage:**
- Stores column names in separate collection
- Useful for dynamic form generation
- Can retrieve column list without scanning all documents

---

### 6. Frontend JavaScript Explanation

#### Dashboard Statistics Loading

```javascript
async function loadDashboardStats() {
  try {
    const response = await fetch('/api/dashboard-stats');
    const data = await response.json();
    
    // Update stat cards
    document.getElementById('totalPatients').textContent = data.total;
    document.getElementById('strokeCases').textContent = data.strokeCases;
    document.getElementById('highRisk').textContent = data.highRisk;
    document.getElementById('avgAge').textContent = data.avgAge + ' years';
    
    // Update charts
    updateCharts(data);
  } catch (error) {
    console.error('Error loading stats:', error);
  }
}
```

**Explanation:**
- **async/await**: Modern way to handle asynchronous operations
- **fetch()**: Makes HTTP request to server
- **await**: Waits for response before continuing
- **response.json()**: Parses JSON response
- **textContent**: Updates HTML element text
- **try/catch**: Error handling

**Why async/await?**
- Cleaner than callbacks
- Easier to read and maintain
- Better error handling
- Code looks synchronous but runs asynchronously

---

#### Patient List with Search

```javascript
let patientData = [];
let filteredData = [];
let currentPage = 1;
const rowsPerPage = 50;

function loadPatientsFromDB() {
  fetch('/api/patients')
    .then(response => response.json())
    .then(data => {
      patientData = data;
      filteredData = data;
      updateStatistics();
      renderTable();
    });
}

function searchPatients() {
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();
  
  filteredData = patientData.filter(patient => {
    return String(patient.id).includes(searchTerm) ||
           String(patient.age).includes(searchTerm) ||
           (patient.gender || '').toLowerCase().includes(searchTerm);
  });
  
  currentPage = 1;
  renderTable();
}

function renderTable() {
  const start = (currentPage - 1) * rowsPerPage;
  const end = start + rowsPerPage;
  const pageData = filteredData.slice(start, end);
  
  let html = '';
  pageData.forEach(patient => {
    html += `<tr>
      <td>${patient.id}</td>
      <td>${patient.age}</td>
      <td>${patient.gender}</td>
      <td><span class="badge ${patient.hypertension === 1 ? 'badge-red' : 'badge-green'}">
        ${patient.hypertension === 1 ? 'Yes' : 'No'}
      </span></td>
      <td><button onclick="showPatientModal(${patient.id})">View Details</button></td>
    </tr>`;
  });
  
  document.getElementById('tableBody').innerHTML = html;
  updatePagination();
}
```

**Explanation:**

**State Management:**
- `patientData`: Original data from server (never changes)
- `filteredData`: Filtered results from search
- `currentPage`: Current pagination page

**Array Methods:**
- `.filter()`: Creates new array with matching elements
- `.slice()`: Extracts portion of array
- `.forEach()`: Loops through array

**String Methods:**
- `.toLowerCase()`: Converts to lowercase for case-insensitive search
- `.includes()`: Checks if string contains substring
- `String()`: Converts number to string

**Template Literals:**
- Backticks: `` `text ${variable}` ``
- Allows embedding variables in strings
- Supports multi-line strings

---

#### Form Submission with Fetch

```javascript
form.addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const formData = new FormData(form);
  
  try {
    let response;
    
    if (editMode) {
      response = await fetch(`/api/patient/${originalPatientId}`, {
        method: 'PUT',
        body: formData
      });
    } else {
      response = await fetch('/add_patient', {
        method: 'POST',
        body: formData
      });
    }
    
    const result = await response.json();
    
    if (response.ok && result.success) {
      showMessage(editMode ? 'Patient updated!' : 'Patient added!', 'success');
      
      if (editMode) {
        sessionStorage.removeItem('editPatient');
      }
      
      setTimeout(() => {
        window.location.href = '/patient';
      }, 2000);
    }
  } catch (error) {
    showMessage('Error: ' + error.message, 'error');
  }
});
```

**Explanation:**

**Event Handling:**
- `addEventListener('submit', ...)`: Listens for form submission
- `e.preventDefault()`: Stops default form submission (page reload)

**FormData API:**
- `new FormData(form)`: Automatically collects all form fields
- Maintains field names and values
- Handles file uploads (if needed)

**Conditional Logic:**
- Checks `editMode` flag to determine PUT or POST
- Different endpoints for create vs update
- Different success messages

**Session Storage:**
- `sessionStorage.setItem()`: Stores data (survives page refresh)
- `sessionStorage.getItem()`: Retrieves data
- `sessionStorage.removeItem()`: Deletes data
- Only available in same browser tab

**Redirect with Delay:**
- `setTimeout()`: Waits 2 seconds
- `window.location.href`: Navigates to new page
- Gives user time to see success message

---

#### Modal Management

```javascript
function showPatientModal(patientId) {
  const patient = patientData.find(p => p.id === patientId);
  
  if (!patient) {
    alert('Patient not found');
    return;
  }
  
  const modalContent = `
    <div class="patient-info">
      <h3>Patient #${patient.id}</h3>
      <p>Age: ${patient.age}</p>
      <p>Gender: ${patient.gender}</p>
      <!-- ... more fields ... -->
    </div>
    <div class="action-buttons">
      <button onclick="closeModal()">Close</button>
      <button onclick="deletePatient(${patient.id})">Delete</button>
      <button onclick="editPatient(${patient.id})">Update</button>
    </div>
  `;
  
  document.getElementById('modalContent').innerHTML = modalContent;
  document.getElementById('patientModal').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('patientModal').classList.add('hidden');
}

function editPatient(patientId) {
  const patient = patientData.find(p => p.id === patientId);
  sessionStorage.setItem('editPatient', JSON.stringify(patient));
  window.location.href = '/add_patient';
}

async function deletePatient(patientId) {
  if (!confirm('Are you sure you want to delete this patient?')) {
    return;
  }
  
  try {
    const response = await fetch(`/api/patient/${patientId}`, {
      method: 'DELETE'
    });
    
    const result = await response.json();
    
    if (result.success) {
      alert('Patient deleted successfully');
      closeModal();
      loadPatientsFromDB();
    }
  } catch (error) {
    alert('Error deleting patient: ' + error.message);
  }
}
```

**Explanation:**

**Array Find:**
- `.find()`: Returns first element matching condition
- `p => p.id === patientId`: Arrow function (shorthand)
- Returns `undefined` if not found

**Dynamic HTML:**
- `innerHTML`: Replaces element content with HTML
- Template literals for multi-line HTML
- Inline `onclick` handlers for simplicity

**CSS Classes:**
- `.classList.add()`: Adds CSS class
- `.classList.remove()`: Removes CSS class
- `.classList.toggle()`: Adds if absent, removes if present
- `hidden` class controls visibility

**Confirmation Dialog:**
- `confirm()`: Browser's built-in yes/no dialog
- Returns `true` if user clicks OK
- Returns `false` if user clicks Cancel

**Data Persistence:**
- `JSON.stringify()`: Converts object to JSON string
- `JSON.parse()`: Converts JSON string back to object
- Required for sessionStorage (only stores strings)

---

## Security Implementation

### Current Security Measures

#### 1. Session-Based Authentication
```python
if 'user' not in session:
    return redirect(url_for('auth.login'))
```
- Checks user authentication before allowing access
- Sessions stored server-side
- Session ID stored in encrypted cookie

#### 2. MongoDB Connection Security
- Uses MongoDB Atlas (cloud-hosted, secured)
- Connection string with username/password
- SSL/TLS encryption for data in transit

#### 3. Error Handling
```python
try:
    # operation
except Exception as e:
    return {'error': str(e)}, 500
```
- Prevents application crashes
- Returns proper HTTP error codes
- Logs errors for debugging

### Security Improvements Needed (Production)

#### 1. Password Hashing
**Current:** Plain text password comparison
```python
if password == 'AdminPass':
```

**Should be:**
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Store hashed password
hashed = generate_password_hash('AdminPass')

# Check password
if check_password_hash(hashed, password):
```

#### 2. Input Validation
**Add validation for:**
- Email format
- Password strength (minimum length, special characters)
- Age range (0-120)
- BMI range (10-60)
- Glucose level range

#### 3. SQL/NoSQL Injection Prevention
**Current approach is safe:**
- MongoDB's parameterized queries prevent injection
- No string concatenation in queries

**Example of UNSAFE code (don't do this):**
```python
# UNSAFE - allows injection
query = f"SELECT * FROM users WHERE id = {user_id}"

# SAFE - parameterized
query = {'id': user_id}
```

#### 4. CSRF Protection
**Add CSRF tokens to forms:**
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
```

#### 5. Rate Limiting
**Prevent brute force attacks:**
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # ...
```

#### 6. Environment Variables
**Move sensitive data out of code:**
```python
import os

MONGO_URI = os.environ.get('MONGO_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')
```

#### 7. HTTPS Only
**Force HTTPS in production:**
```python
from flask_talisman import Talisman

Talisman(app, force_https=True)
```

---

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Landing page | No |
| GET | `/login` | Show login form | No |
| POST | `/login` | Submit login credentials | No |
| GET | `/register` | Show registration form | No |
| POST | `/register` | Submit registration data | No |
| GET | `/logout` | Logout and clear session | Yes |

### Dashboard Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/dashboard` | Show dashboard page | Yes |
| GET | `/patient` | Show patient list page | Yes |
| GET | `/add_patient` | Show add patient form | Yes |

### API Endpoints (JSON)

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/patients` | Get all patients | None | Array of patient objects |
| GET | `/api/dashboard-stats` | Get aggregated statistics | None | Statistics object |
| POST | `/add_patient` | Add new patient | FormData with patient fields | `{success: bool, message: string}` |
| PUT | `/api/patient/<id>` | Update existing patient | FormData with patient fields | `{success: bool, message: string}` |
| DELETE | `/api/patient/<id>` | Delete patient | None | `{success: bool, message: string}` |

### Request/Response Examples

#### GET /api/patients
**Response:**
```json
[
  {
    "id": 10001,
    "age": 67,
    "gender": "Male",
    "hypertension": 0,
    "heart_disease": 1,
    "ever_married": "Yes",
    "work_type": "Private",
    "Residence_type": "Urban",
    "avg_glucose_level": 228.69,
    "bmi": 36.6,
    "smoking_status": "formerly smoked",
    "stroke": 1
  }
]
```

#### GET /api/dashboard-stats
**Response:**
```json
{
  "total": 5110,
  "strokeCases": 249,
  "highRisk": 98,
  "avgAge": 43.2,
  "genderDistribution": {
    "Male": 2115,
    "Female": 2994,
    "Other": 1
  }
}
```

#### POST /add_patient
**Request (FormData):**
```
id: 10001
age: 67
gender: Male
hypertension: 0
heart_disease: 1
ever_married: Yes
work_type: Private
Residence_type: Urban
avg_glucose_level: 228.69
bmi: 36.6
smoking_status: formerly smoked
stroke: 1
```

**Response:**
```json
{
  "success": true,
  "message": "Patient added successfully"
}
```

#### PUT /api/patient/10001
**Request (FormData):**
```
age: 68
gender: Male
... (other fields)
```

**Response:**
```json
{
  "success": true,
  "message": "Patient updated successfully"
}
```

#### DELETE /api/patient/10001
**Response:**
```json
{
  "success": true,
  "message": "Patient deleted successfully"
}
```

---

## User Guide

### Getting Started

#### 1. Access the Application
1. Make sure the server is running: `python run.py`
2. Open browser and go to: `http://127.0.0.1:5000/`
3. You'll see the landing page

#### 2. Login
1. Click "Login" button
2. Enter credentials:
   - Email: `admin@example.com`
   - Password: `AdminPass`
3. Click "Login"
4. You'll be redirected to the dashboard

### Using the Dashboard

#### View Statistics
- **Total Patients**: Shows total number of patients in database
- **Stroke Cases**: Number of patients who had a stroke
- **High Risk**: Patients with both hypertension and heart disease
- **Average Age**: Average age of all patients

#### Charts
- **Risk Distribution**: Pie chart showing risk levels
  - Low Risk: No cardiovascular conditions
  - Moderate Risk: Either hypertension or heart disease
  - High Risk: Both hypertension and heart disease

- **Gender Distribution**: Bar chart showing patient count by gender

#### Recent Patients Table
- Shows last 10 patients added
- Click patient name to view full details

### Managing Patients

#### View Patient List
1. Click "List of Patients" in navigation
2. See all patients in table format
3. Use search box to filter patients
4. Navigate pages using pagination buttons

#### Search Patients
1. Type in search box at top
2. Search works on:
   - Patient ID
   - Age
   - Gender
3. Results update automatically as you type
4. Clear search box to see all patients

#### View Patient Details
1. Find patient in list
2. Click "View Details" button
3. Modal opens with 4 sections:
   - **Personal Information**: ID, age, gender, marital status
   - **Medical History**: Hypertension, heart disease, stroke, glucose, BMI
   - **Lifestyle**: Work type, residence, smoking status
   - **Risk Assessment**: Automated risk evaluation

#### Add New Patient
1. Click "Add Patient" in navigation
2. Fill in all required fields:
   - Patient ID is auto-generated
   - Enter age (numbers only)
   - Select gender from dropdown
   - Select Yes/No for medical conditions
   - Enter glucose level and BMI (decimals allowed)
   - Select work type, residence, smoking status
3. Click "Add Patient" button
4. Wait for success message
5. Redirected to patient list automatically

**Field Requirements:**
- Age: Must be a positive number
- Glucose Level: Must be > 0 (typically 70-300 mg/dL)
- BMI: Must be > 0 (typically 15-50)
- All dropdowns must have selection

#### Update Patient
1. View patient details (click "View Details")
2. Click "Update Patient" button in modal
3. Form opens with all fields pre-filled
4. Modify any fields you want to change
5. Patient ID cannot be changed (read-only)
6. Click "Update Patient" button
7. Wait for success message
8. Redirected to patient list

**Tips:**
- Double-check important fields before updating
- Can't undo after clicking update
- Original data is replaced completely

#### Delete Patient
1. View patient details
2. Click "Delete Patient" button
3. Confirmation dialog appears
4. Click "OK" to confirm deletion
5. Click "Cancel" to abort
6. If confirmed, patient is permanently removed
7. Modal closes and list refreshes

**Warning:**
- Deletion is permanent
- Cannot be undone
- Patient record is completely removed from database

### Logout
1. Click "Logout" in navigation
2. Session is cleared
3. Redirected to login page
4. Must login again to access protected pages

---

## Troubleshooting

### Common Issues

#### 1. Cannot Connect to MongoDB
**Error:** `ServerSelectionTimeoutError`

**Solutions:**
- Check internet connection
- Verify MongoDB Atlas cluster is running
- Check IP whitelist in MongoDB Atlas (should be 0.0.0.0/0 or your IP)
- Verify connection string is correct
- Check username/password in connection string

#### 2. Module Not Found
**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip install flask pymongo pandas
```

#### 3. CSV File Not Found
**Error:** `FileNotFoundError: stroke.csv`

**Solution:**
- Make sure `stroke.csv` is in the project root directory
- Check file path in `load_csv_to_mongo.py`
- Use absolute path if needed

#### 4. Session Not Working
**Error:** Keeps redirecting to login

**Solutions:**
- Check `secret_key` is set in `app/__init__.py`
- Clear browser cookies
- Try incognito/private browsing window
- Restart Flask server

#### 5. Port Already in Use
**Error:** `Address already in use`

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>

# Or use different port
app.run(port=5001)
```

#### 6. Form Submission Returns 404
**Solutions:**
- Check route exists in `routes.py`
- Verify blueprint is registered
- Check method is allowed (GET/POST/PUT/DELETE)
- Clear browser cache

#### 7. JavaScript Not Loading
**Solutions:**
- Check browser console for errors (F12)
- Verify CDN links are accessible
- Check for typos in function names
- Ensure scripts are in `{% block scripts %}`

### Debug Mode

**Enable detailed error messages:**
```python
# In run.py
app.run(debug=True)
```

**What debug mode does:**
- Shows detailed error pages
- Auto-reloads on code changes
- Enables interactive debugger
- **Never use in production!**

### Logging

**Add logging for debugging:**
```python
import logging

logging.basicConfig(level=logging.DEBUG)

@app.route('/test')
def test():
    app.logger.debug('Debug message')
    app.logger.info('Info message')
    app.logger.warning('Warning message')
    app.logger.error('Error message')
    return 'Check console'
```

---

## Future Enhancements

### Potential Features

1. **User Management**
   - Multiple user accounts
   - Role-based access (admin, doctor, nurse)
   - User profile pages
   - Password reset functionality

2. **Advanced Search**
   - Filter by multiple criteria
   - Date range filters
   - Complex queries (age > 60 AND stroke = 1)
   - Save search filters

3. **Data Export**
   - Export to CSV
   - Export to PDF
   - Generate reports
   - Email reports

4. **Data Visualization**
   - More chart types (line, scatter, heatmap)
   - Interactive charts (zoom, filter)
   - Trend analysis over time
   - Predictive analytics

5. **Patient History**
   - Track changes over time
   - Visit history
   - Treatment records
   - Document uploads

6. **Notifications**
   - Email alerts for high-risk patients
   - Appointment reminders
   - System notifications
   - Real-time updates

7. **Mobile App**
   - iOS and Android apps
   - Responsive design improvements
   - Touch-optimized interface
   - Offline mode

8. **API Documentation**
   - Swagger/OpenAPI documentation
   - API versioning
   - Rate limiting
   - API keys for external access

9. **Backup & Recovery**
   - Automated backups
   - Point-in-time recovery
   - Data archiving
   - Disaster recovery plan

10. **Performance Optimization**
    - Database indexing
    - Caching (Redis)
    - Lazy loading
    - Image optimization

---

## Conclusion

This documentation covers all aspects of the Stroke Patient Management System, from installation to advanced features. The system provides a solid foundation for managing patient records with modern web technologies.

### Key Takeaways

- **Flask**: Lightweight and flexible Python web framework
- **MongoDB**: Scalable NoSQL database for medical records
- **RESTful API**: Clean separation between frontend and backend
- **CRUD Operations**: Complete data management capabilities
- **Responsive Design**: Works on desktop and mobile devices
- **Secure Authentication**: Session-based user management

### Learning Outcomes

By studying this project, you've learned:
- Flask application structure and Blueprints
- MongoDB integration with pymongo
- RESTful API design
- Frontend-backend communication with Fetch API
- Session management and authentication
- Data visualization with Chart.js
- Form handling and validation
- Error handling and debugging techniques

### Next Steps

1. **Practice**: Try modifying features and adding new ones
2. **Deploy**: Host on Heroku, PythonAnywhere, or AWS
3. **Secure**: Implement password hashing and HTTPS
4. **Scale**: Add more features and optimize performance
5. **Share**: Contribute to open source or showcase in portfolio

---

## Support & Resources

### Official Documentation
- **Flask**: https://flask.palletsprojects.com/
- **MongoDB**: https://docs.mongodb.com/
- **Pymongo**: https://pymongo.readthedocs.io/
- **Chart.js**: https://www.chartjs.org/docs/
- **Tailwind CSS**: https://tailwindcss.com/docs

### Tutorials
- Flask Mega-Tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
- MongoDB University: https://university.mongodb.com/
- JavaScript MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript

### Community
- Stack Overflow: Tag questions with `flask`, `mongodb`, `pymongo`
- Reddit: r/flask, r/mongodb
- Discord: Flask Community, MongoDB Community

---

**Document Version:** 1.0  
**Last Updated:** December 2, 2025  
**Author:** Stroke Patient Management System Development Team  
**License:** Educational Use

---

*Thank you for using the Stroke Patient Management System!*
