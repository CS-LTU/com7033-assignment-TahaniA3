from flask import Flask, app

def create_app():
    app = Flask(__name__)
    # Secret key for session encryption
    app.secret_key = 'your-secret-key-change-this-in-production-123456'
    from app import routes
    app.register_blueprint(routes.auth_bp)
    app.register_blueprint(routes.dashboard_bp)

    return app