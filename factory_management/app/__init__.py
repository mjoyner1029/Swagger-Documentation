from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restplus import Api

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
api = Api(version='1.0', title='Factory Management System API',
          description='A comprehensive API for managing factory operations')

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    limiter.init_app(app)
    api.init_app(app)
    
    from app.routes.employees import bp as employees_bp
    from app.routes.products import bp as products_bp
    from app.routes.orders import bp as orders_bp
    from app.routes.customers import bp as customers_bp
    from app.routes.production import bp as production_bp
    
    app.register_blueprint(employees_bp, url_prefix='/employees')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(production_bp, url_prefix='/production')
    
    return app
