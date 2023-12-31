from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    jwt = JWTManager(app)

    # Register blueprints here
    from app.api import bp as api_bp
    from app.admin import bp as admin_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/admin/api")

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app