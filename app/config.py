import pymongo
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId  
from datetime import datetime


# MongoDB client connection
client = MongoClient('mongodb+srv://taalanzi35_db_user:TaaH-11233@stroke.xsvmyml.mongodb.net/')
server_info = client.server_info()

mongo_version = server_info["version"]

print(f"mongoDB version: {mongo_version}")


# Multiple Interconnected Databases Setup

# Database 1: User Management Database
# Handles authentication, user profiles, and access control
auth_db = client["user_management_db"]
users_collection = auth_db["users"]
user_sessions_collection = auth_db["sessions"]  # Track active sessions

# Database 2: Patient Records Database
# Stores all patient medical records and health data
patient_db = client["stroke_patient_db"]
collection = patient_db["patients"]  # Main patient records
patient_history_collection = patient_db["patient_history"]  # Track changes to patient records

# Database 3: Audit and Logging Database
# Records all system activities for security and compliance
audit_db = client["audit_logs_db"]
access_logs_collection = audit_db["access_logs"]  # Who accessed what and when
data_changes_collection = audit_db["data_changes"]  # Track all CRUD operations

# Legacy compatibility - keep 'collection' name for existing code
# This points to the patient records in the patient database 

