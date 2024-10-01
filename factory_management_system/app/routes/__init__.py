from flask import Blueprint

# Create a blueprint for the routes
bp = Blueprint('api', __name__)

# Import the route files
from app.routes import employee, product, order, customer, production
