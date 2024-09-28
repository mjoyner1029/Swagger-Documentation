from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes import employee, product, order, customer, production

db = SQLAlchemy()
limiter = Limiter()

# Swagger settings
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Path to your Swagger JSON file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Factory Management System API"
    }
)

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(employee.bp)
    app.register_blueprint(product.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(customer.bp)
    app.register_blueprint(production.bp)

    # Register Swagger UI blueprint
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    return app
