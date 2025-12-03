"""
Initialize admin user in MongoDB database.
Run this script once to create the default admin account.
"""

from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# MongoDB connection
MONGO_URI = "mongodb+srv://taalanzi35_db_user:TaaH-11233@stroke.xsvmyml.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['stroke_database']
users_collection = db['users']

def create_admin_user():
    """Create default admin user if it doesn't exist."""
    
    # Check if admin already exists
    existing_admin = users_collection.find_one({'email': 'admin@example.com'})
    
    if existing_admin:
        print("Admin user already exists!")
        return
    
    # Create admin user
    admin_data = {
        'email': 'admin@example.com',
        'password': generate_password_hash('AdminPass'),  # Password is hashed
        'fullName': 'Admin User',
        'role': 'admin'
    }
    
    try:
        users_collection.insert_one(admin_data)
        print("✅ Admin user created successfully!")
        print("Email: admin@example.com")
        print("Password: AdminPass")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

if __name__ == '__main__':
    print("Initializing admin user...")
    create_admin_user()
    print("\nYou can now login with:")
    print("  Email: admin@example.com")
    print("  Password: AdminPass")
