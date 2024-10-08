from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes import bp as api_bp

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)

# Swagger settings
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'  # Path to your Swagger YAML file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Factory Management System API"
    }
)

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    db.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(api_bp)

    # Register Swagger UI blueprint
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    return app
