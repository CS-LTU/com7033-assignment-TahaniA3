"""
Security utilities for input sanitization and validation.
Implements XSS prevention, NoSQL injection prevention, and secure data handling.
"""
import bleach
import re
from bson.objectid import ObjectId


class SecurityUtils:
    """Security utilities for input validation and sanitization."""
    
    # Allowed HTML tags for rich text (if needed in future)
    ALLOWED_TAGS = []
    ALLOWED_ATTRIBUTES = {}
    
    @staticmethod
    def sanitize_html(text):
        """
        Sanitize HTML input to prevent XSS attacks.
        Removes all HTML tags and dangerous content.
        """
        if not text or not isinstance(text, str):
            return text
        
        # Remove all HTML tags
        return bleach.clean(text, tags=SecurityUtils.ALLOWED_TAGS, 
                          attributes=SecurityUtils.ALLOWED_ATTRIBUTES, 
                          strip=True)
    
    @staticmethod
    def sanitize_input(data):
        """
        Recursively sanitize all string inputs in data structures.
        Prevents XSS by escaping HTML.
        """
        if isinstance(data, dict):
            return {k: SecurityUtils.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [SecurityUtils.sanitize_input(item) for item in data]
        elif isinstance(data, str):
            return SecurityUtils.sanitize_html(data)
        else:
            return data
    
    @staticmethod
    def prevent_nosql_injection(query):
        """
        Prevent NoSQL injection in MongoDB queries.
        Validates that query operators are safe.
        """
        if isinstance(query, dict):
            for key in query.keys():
                # Block dangerous MongoDB operators
                if key.startswith('$') and key not in ['$set', '$push', '$pull', '$inc']:
                    raise ValueError(f"Potentially dangerous operator detected: {key}")
                
                # Recursively check nested queries
                if isinstance(query[key], dict):
                    SecurityUtils.prevent_nosql_injection(query[key])
        
        return query
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format to prevent injection.
        Returns sanitized email or raises ValueError.
        """
        if not email or not isinstance(email, str):
            raise ValueError("Invalid email format")
        
        # Sanitize first
        email = SecurityUtils.sanitize_html(email).strip().lower()
        
        # Validate email pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        # Check for dangerous characters
        if any(char in email for char in ['<', '>', '"', "'", ';', '--', '/*', '*/']):
            raise ValueError("Email contains invalid characters")
        
        return email
    
    @staticmethod
    def validate_password(password):
        """
        Validate password strength and format.
        """
        if not password or not isinstance(password, str):
            raise ValueError("Password is required")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Check for common weak passwords
        weak_passwords = ['password', '12345678', 'qwerty', 'admin123']
        if password.lower() in weak_passwords:
            raise ValueError("Password is too weak")
        
        return True
    
    @staticmethod
    def validate_patient_id(patient_id):
        """
        Validate patient ID to prevent injection.
        """
        try:
            patient_id = int(patient_id)
            if patient_id < 0:
                raise ValueError("Patient ID must be positive")
            return patient_id
        except (ValueError, TypeError):
            raise ValueError("Invalid patient ID format")
    
    @staticmethod
    def validate_numeric_field(value, field_name, min_val=None, max_val=None):
        """
        Validate numeric fields with range checking.
        """
        try:
            if value is None or value == '':
                return None
            
            # Try to convert to float
            num_val = float(value)
            
            # Check range
            if min_val is not None and num_val < min_val:
                raise ValueError(f"{field_name} must be at least {min_val}")
            if max_val is not None and num_val > max_val:
                raise ValueError(f"{field_name} must be at most {max_val}")
            
            return num_val
        except (ValueError, TypeError):
            raise ValueError(f"Invalid {field_name} format")
    
    @staticmethod
    def validate_patient_data(data):
        """
        Comprehensive validation of patient data.
        Prevents injection and ensures data integrity.
        """
        validated_data = {}
        
        # Validate and sanitize required fields
        required_fields = ['id', 'gender', 'age']
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                raise ValueError(f"{field} is required")
        
        # Validate patient ID
        validated_data['id'] = SecurityUtils.validate_patient_id(data['id'])
        
        # Validate age
        validated_data['age'] = SecurityUtils.validate_numeric_field(
            data.get('age'), 'Age', min_val=0, max_val=150
        )
        
        # Validate and sanitize gender
        gender = SecurityUtils.sanitize_html(str(data.get('gender', ''))).strip()
        if gender not in ['Male', 'Female', 'Other']:
            raise ValueError("Invalid gender value")
        validated_data['gender'] = gender
        
        # Validate binary fields (0 or 1)
        binary_fields = ['hypertension', 'heart_disease', 'stroke']
        for field in binary_fields:
            value = data.get(field, 0)
            try:
                value = int(value)
                if value not in [0, 1]:
                    raise ValueError
                validated_data[field] = value
            except (ValueError, TypeError):
                raise ValueError(f"Invalid {field} value (must be 0 or 1)")
        
        # Validate and sanitize text fields
        text_fields = ['ever_married', 'work_type', 'Residence_type', 'smoking_status']
        for field in text_fields:
            value = data.get(field, '')
            if value:
                validated_data[field] = SecurityUtils.sanitize_html(str(value)).strip()
        
        # Validate numeric fields with ranges
        validated_data['avg_glucose_level'] = SecurityUtils.validate_numeric_field(
            data.get('avg_glucose_level'), 'Average Glucose Level', min_val=0, max_val=500
        )
        
        validated_data['bmi'] = SecurityUtils.validate_numeric_field(
            data.get('bmi'), 'BMI', min_val=0, max_val=100
        )
        
        return validated_data
    
    @staticmethod
    def safe_objectid(id_string):
        """
        Safely convert string to MongoDB ObjectId.
        """
        try:
            return ObjectId(id_string)
        except Exception:
            raise ValueError("Invalid ObjectId format")
