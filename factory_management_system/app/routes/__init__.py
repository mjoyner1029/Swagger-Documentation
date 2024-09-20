from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_swagger import swagger
from app.routes import employee, product, order, customer, production

db = SQLAlchemy()
limiter = Limiter()

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

    @app.route("/swagger")
    def swagger_spec():
        return swagger(app)

    return app
