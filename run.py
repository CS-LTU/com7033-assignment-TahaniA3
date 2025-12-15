"""
Application Entry Point
=======================
This is the main entry point for the Stroke Patient Management System.
It initializes and runs the Flask application with all security configurations.

Usage:
    python run.py

The application will start on http://127.0.0.1:5000 in debug mode.
Debug mode provides:
    - Auto-reload on code changes
    - Detailed error messages
    - Interactive debugger

WARNING: Debug mode should NEVER be enabled in production!

Author: Tahani A3
Course: COM7033 - Secure Software Development
Institution: Leeds Trinity University
"""

from app import create_app

# Create Flask application instance using the factory pattern
# This approach allows for better testing and multiple app configurations
app = create_app()

if __name__ == '__main__':
    # Start the development server
    # debug=True enables:
    #   - Automatic reloading when code changes
    #   - Enhanced error messages with stack traces
    #   - Interactive debugger in browser
    # 
    # For production deployment, use a WSGI server like Gunicorn:
    #   gunicorn -w 4 -b 0.0.0.0:8000 run:app
    app.run(debug=True)