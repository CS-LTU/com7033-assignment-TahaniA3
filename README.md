# Stroke Patient Management System

A secure, enterprise-grade web application for managing stroke patient records with comprehensive medical data tracking, statistical analysis, and multi-database architecture.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.2-green.svg)
![MongoDB](https://img.shields.io/badge/mongodb-8.0.16-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Security Features](#security-features)
- [Database Architecture](#database-architecture)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)

## 🎯 Overview

This Flask-based web application provides healthcare administrators with a secure platform to manage patient stroke records. The system features a modern glass-morphism UI, real-time statistics dashboard, comprehensive CRUD operations, and enterprise-grade security measures including CSRF protection, rate limiting, and input sanitization.

### Key Highlights
- ✅ **5,110+ patient records** with 12 medical attributes
- ✅ **Multi-database architecture** (3 interconnected databases)
- ✅ **Enterprise security** (CSRF, rate limiting, XSS prevention)
- ✅ **54 unit tests** with comprehensive coverage
- ✅ **Real-time analytics** with Chart.js visualizations
- ✅ **RESTful API** for data access and manipulation

## ✨ Features

### 🔐 Authentication & Authorization
- Secure user registration and login
- Password hashing (PBKDF2-SHA256 with 16-byte salt)
- Session management with timeout (1 hour)
- Role-based access control (user/admin)
- Secure cookie configuration (HTTPOnly, SameSite)

### 📊 Dashboard & Analytics
- Real-time patient statistics
- Interactive charts (stroke distribution, gender breakdown, age distribution)
- Risk factor analysis
- Patient demographics visualization

### 🏥 Patient Management
- **Create**: Add new patient records with validation
- **Read**: Browse patient list with search functionality
- **Update**: Edit existing patient information
- **Delete**: Remove patient records with audit logging
- Duplicate prevention
- Comprehensive input validation

### 🛡️ Security Features
- CSRF protection on all forms
- Rate limiting (brute force prevention)
- Input sanitization (XSS prevention)
- NoSQL injection prevention
- Security headers (CSP, HSTS, X-Frame-Options)
- Audit logging for all operations

### 📈 API Endpoints
- GET `/api/patients` - Fetch all patient records
- GET `/api/stats` - Get dashboard statistics
- POST `/api/update_patient` - Update patient data
- POST `/api/delete_patient` - Delete patient record
- GET `/api/my-activity-report` - User activity report
- GET `/api/database-status` - Database health check

## 🛠️ Technology Stack

### Backend
- **Flask 3.1.2** - Web framework
- **Python 3.8+** - Programming language
- **PyMongo** - MongoDB driver
- **Pandas** - Data processing
- **Werkzeug** - Password hashing and security

### Frontend
- **HTML5** - Markup
- **Tailwind CSS** - Styling framework
- **JavaScript (ES6+)** - Client-side logic
- **Chart.js** - Data visualization

### Database
- **MongoDB Atlas 8.0.16** - Cloud NoSQL database
- **3 Databases**:
  - `user_management_db` - Authentication and sessions
  - `stroke_patient_db` - Patient records and history
  - `audit_logs_db` - Access logs and data changes

### Security
- **Flask-WTF 1.2.2** - CSRF protection
- **Flask-Limiter 4.1.0** - Rate limiting
- **bleach 6.3.0** - HTML sanitization
- **python-dotenv 1.2.1** - Environment configuration

### Testing
- **pytest 9.0.1** - Testing framework
- **pytest-cov 7.0.0** - Code coverage

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account (free tier available)
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/CS-LTU/com7033-assignment-TahaniA3.git
cd com7033-assignment-TahaniA3
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install flask pymongo pandas werkzeug
pip install Flask-WTF Flask-Limiter python-dotenv bleach
```

Or use requirements file:
```bash
pip install -r tests/requirements.txt
```

### Step 4: Configure Environment
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
RATELIMIT_STORAGE_URL=memory://
```

### Step 5: Initialize Database
```bash
# Setup multi-database architecture
python scripts/setup_multi_databases.py

# Load patient data from CSV
python scripts/load_csv_to_mongo.py

# Create admin user (optional)
python scripts/init_admin.py
```

### Step 6: Run Application
```bash
python run.py
```

Visit: `http://127.0.0.1:5000`

## ⚙️ Configuration

### MongoDB Atlas Setup

1. **Create Cluster**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create free M0 cluster

2. **Database Access**
   - Add database user with read/write permissions
   - Note username and password

3. **Network Access**
   - Add IP address: `0.0.0.0/0` (allow from anywhere)
   - Or add your specific IP

4. **Connection String**
   - Get connection string from "Connect" → "Connect your application"
   - Update `MONGO_URI` in `.env` file

### Application Settings

Edit `app/config.py` for advanced configuration:
- Database names
- Collection names
- Session timeout
- Rate limit rules

## 🚀 Usage

### Default Credentials
```
Email: admin@example.com
Password: AdminPass123
```

### User Workflow

1. **Login** (`/login`)
   - Enter credentials
   - System creates secure session

2. **Dashboard** (`/dashboard`)
   - View patient statistics
   - Analyze charts and trends
   - Monitor high-risk patients

3. **Patient List** (`/patient`)
   - Browse all patients
   - Search by name or ID
   - View detailed information

4. **Add Patient** (`/add_patient`)
   - Fill patient form
   - System validates input
   - Duplicate prevention

5. **Update/Delete**
   - Edit patient details
   - Delete records (with confirmation)
   - All changes logged for audit

### API Usage

```javascript
// Fetch all patients
fetch('/api/patients')
  .then(response => response.json())
  .then(data => console.log(data));

// Get statistics
fetch('/api/stats')
  .then(response => response.json())
  .then(stats => {
    console.log('Total:', stats.total_patients);
    console.log('Stroke %:', stats.stroke_percentage);
  });

// Update patient
fetch('/api/update_patient', {
  method: 'POST',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: 'id=12345&age=50&bmi=28.5'
});
```

## 🔒 Security Features

### Implemented Security Measures

1. **CSRF Protection**
   - Flask-WTF tokens on all forms
   - Prevents cross-site request forgery

2. **Rate Limiting**
   - Login: 5 attempts/minute
   - Registration: 3 attempts/minute
   - Patient operations: 10/minute

3. **Input Sanitization**
   - HTML tag stripping (bleach)
   - XSS prevention
   - Email validation with regex
   - Numeric field validation

4. **Password Security**
   - PBKDF2-SHA256 hashing
   - 16-byte salt
   - Minimum 8 characters
   - Weak password detection

5. **Session Security**
   - HTTPOnly cookies
   - SameSite=Lax
   - 1-hour timeout
   - Secure session IDs (256-bit)

6. **Security Headers**
   - Content-Security-Policy
   - X-Content-Type-Options: nosniff
   - X-Frame-Options: DENY
   - X-XSS-Protection: 1; mode=block
   - Strict-Transport-Security

7. **NoSQL Injection Prevention**
   - Query operator validation
   - Input type checking
   - Safe ObjectId conversion

## 🗄️ Database Architecture

### Three Interconnected Databases

```
┌─────────────────────────────────────────────────┐
│         user_management_db                      │
│  ├── users (authentication, profiles)           │
│  └── sessions (active sessions tracking)        │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│         stroke_patient_db                       │
│  ├── patients (main patient records)            │
│  └── patient_history (change tracking)          │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│         audit_logs_db                           │
│  ├── access_logs (who accessed what)            │
│  └── data_changes (all CRUD operations)         │
└─────────────────────────────────────────────────┘
```

**Benefits:**
- Data separation and security
- Scalability (independent scaling)
- Compliance (audit trail separation)
- Performance (optimized queries)

See [MULTI_DATABASE_ARCHITECTURE.md](MULTI_DATABASE_ARCHITECTURE.md) for details.

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_routes.py -v
pytest tests/test_config.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

### Test Coverage
- **54 test cases** total
- Authentication tests (8 tests)
- Dashboard access tests (4 tests)
- Patient CRUD tests (9 tests)
- Security tests (3 tests)
- Input validation tests (3 tests)
- Database tests (15 tests)

See [tests/README.md](tests/README.md) for testing documentation.

## 📚 Documentation

### Available Documentation

- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete system documentation (1,759 lines)
  - Installation guide
  - Feature descriptions
  - Code explanations
  - User guide

- **[MULTI_DATABASE_ARCHITECTURE.md](MULTI_DATABASE_ARCHITECTURE.md)** - Database design
  - Architecture overview
  - Collection schemas
  - Cross-database operations
  - Setup instructions

- **[ADVANCED_SECURITY_GUIDE.md](ADVANCED_SECURITY_GUIDE.md)** - Security implementation
  - Security features
  - Best practices
  - Threat prevention
  - Configuration guide

- **[SECURITY_IMPLEMENTATION.md](SECURITY_IMPLEMENTATION.md)** - Security details
  - Implementation specifics
  - Code examples
  - Testing security

- **[tests/README.md](tests/README.md)** - Testing guide
  - Test structure
  - How to run tests
  - Writing new tests

## 📊 Project Statistics

- **Total Lines of Code**: ~3,000+
- **Python Files**: 10+
- **HTML Templates**: 7
- **Test Cases**: 54
- **Documentation**: 5 markdown files
- **Git Commits**: 8 with detailed messages
- **Patient Records**: 5,110+
- **Medical Attributes**: 12 per patient

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install pytest pytest-cov black flake8

# Run code formatter
black app/ tests/

# Run linter
flake8 app/ tests/

# Run tests
pytest tests/ -v
```

### Commit Guidelines
- Use descriptive commit messages
- Follow existing code style
- Add tests for new features
- Update documentation

## 📝 License

This project is part of the COM7033 Secure Software Development course at Leeds Trinity University.

## 👥 Author

**Tahani A3**  
GitHub: [CS-LTU/com7033-assignment-TahaniA3](https://github.com/CS-LTU/com7033-assignment-TahaniA3)

## 🙏 Acknowledgments

- Leeds Trinity University - Computer Science Department
- COM7033 - Secure Software Development Course
- MongoDB Atlas - Database hosting
- Flask Community - Web framework

---

**For detailed information, see [DOCUMENTATION.md](DOCUMENTATION.md)**
