"""
Database Configuration Module
==============================
This module handles all database connections and collection references for the
Stroke Patient Management System. It implements a multi-database architecture
for better security, scalability, and data separation.

Architecture:
    - user_management_db: Authentication and user profiles
    - stroke_patient_db: Patient medical records
    - audit_logs_db: Security audit trails and access logs

Security Features:
    - Separate databases for different data types
    - Audit logging for compliance
    - Session tracking for security monitoring

Connection:
    MongoDB Atlas (Cloud Database Service)
    Version: 8.0.16
    Cluster: stroke.xsvmyml.mongodb.net

Author: Tahani A3
Course: COM7033 - Secure Software Development
"""

import pymongo
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId  
from datetime import datetime

# ============================================================================
# MongoDB Atlas Connection
# ============================================================================
# Establishes connection to MongoDB Atlas cloud database
# Connection string includes credentials and cluster information
# For production: Use environment variables instead of hardcoded credentials
MONGO_URI = 'mongodb+srv://taalanzi35_db_user:TaaH-11233@stroke.xsvmyml.mongodb.net/'
client = MongoClient(MONGO_URI)

# Verify connection and get server information
server_info = client.server_info()
mongo_version = server_info["version"]
print(f"mongoDB version: {mongo_version}")


# ============================================================================
# Multi-Database Architecture Setup
# ============================================================================
# This application uses THREE separate interconnected databases for:
#   1. Security through data separation
#   2. Scalability (each DB can scale independently)
#   3. Compliance (separate audit logs)
#   4. Performance (optimized queries per database)

# ----------------------------------------------------------------------------
# Database 1: User Management Database
# ----------------------------------------------------------------------------
# Purpose: Handles all authentication, authorization, and user management
# Collections:
#   - users: User profiles (email, password hash, role, etc.)
#   - sessions: Active user sessions for security tracking
# Security: Password hashes using PBKDF2-SHA256
auth_db = client["user_management_db"]
users_collection = auth_db["users"]  # User authentication and profiles
user_sessions_collection = auth_db["sessions"]  # Track active sessions with timestamps

# ----------------------------------------------------------------------------
# Database 2: Patient Records Database
# ----------------------------------------------------------------------------
# Purpose: Stores all patient medical records and healthcare data
# Collections:
#   - patients: Main patient records (5,110+ records)
#   - patient_history: Historical changes for audit trail
# Data: Age, gender, hypertension, heart disease, stroke status, BMI, etc.
patient_db = client["stroke_patient_db"]
collection = patient_db["patients"]  # Main patient records (current data)
patient_history_collection = patient_db["patient_history"]  # Historical changes for tracking

# ----------------------------------------------------------------------------
# Database 3: Audit and Logging Database
# ----------------------------------------------------------------------------
# Purpose: Records all system activities for security monitoring and compliance
# Collections:
#   - access_logs: Tracks WHO accessed WHAT and WHEN
#   - data_changes: Records all CRUD operations (Create, Read, Update, Delete)
# Compliance: Meets HIPAA and GDPR audit requirements
audit_db = client["audit_logs_db"]
access_logs_collection = audit_db["access_logs"]  # User activity logs
data_changes_collection = audit_db["data_changes"]  # Data modification audit trail

# ----------------------------------------------------------------------------
# Legacy Compatibility
# ----------------------------------------------------------------------------
# 'collection' variable maintained for backward compatibility with existing code
# Points to the main patient records collection in stroke_patient_db 

