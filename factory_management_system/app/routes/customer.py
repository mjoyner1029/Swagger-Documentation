from flask import Blueprint, request, jsonify
from app.models import db, Customer
from flask_limiter import Limiter

bp = Blueprint('customer', __name__)
limiter = Limiter()

@bp.route('/customers', methods=['POST'])
@limiter.limit("10 per minute")
def create_customer():
    """Create a new customer."""
    data = request.json
    new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'id': new_customer.id, 'name': new_customer.name, 'email': new_customer.email, 'phone': new_customer.phone}), 201

@bp.route('/customers', methods=['GET'])
def get_customers():
    """Get all customers."""
    customers = Customer.query.all()
    return jsonify([{'id': cust.id, 'name': cust.name, 'email': cust.email, 'phone': cust.phone} for cust in customers]), 200
