from flask import Flask, app

def create_app():
    app = Flask(__name__)
    from app import routes
    app.register_blueprint(routes.auth_bp)
    app.register_blueprint(routes.dashboard_bp)

    return app