from flask import Blueprint

# Create a blueprint for the routes
bp = Blueprint('api', __name__)

# Import the route files
from app.routes import employee, product, order, customer, production

# Register the blueprints
bp.register_blueprint(employee.bp)
bp.register_blueprint(product.bp)
bp.register_blueprint(order.bp)
bp.register_blueprint(customer.bp)
bp.register_blueprint(production.bp)
