from flask import Blueprint, request, jsonify
from app.models import db, Customer

bp = Blueprint('customer', __name__)

@bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone': customer.phone}), 201

@bp.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': cust.id, 'name': cust.name, 'email': cust.email, 'phone': cust.phone} for cust in customers]), 200
