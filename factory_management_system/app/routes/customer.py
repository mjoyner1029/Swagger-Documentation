from flask import Blueprint, request, jsonify
from app.models import db, Customer

bp = Blueprint('customer', __name__)

@bp.route('/customers', methods=['POST'])
@limiter.limit("10 per minute")
def create_customer():
    """Create a new customer.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Customer
          properties:
            name:
              type: string
              example: "Jane Doe"
            email:
              type: string
              example: "jane.doe@example.com"
            phone:
              type: string
              example: "123-456-7890"
    responses:
      201:
        description: Customer created successfully
        schema:
          id: CustomerResponse
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
            phone:
              type: string
      400:
        description: Invalid input
        schema:
          id: ErrorResponse
          properties:
            error:
              type: string
            message:
              type: string
    """
    data = request.json
    new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'id': new_customer.id}), 201

@bp.route('/customers', methods=['GET'])
def get_customers():
    """Get all customers.
    ---
    responses:
      200:
        description: A list of customers
        schema:
          type: array
          items:
            id: Customer
            properties:
              id:
                type: integer
              name:
                type: string
              email:
                type: string
              phone:
                type: string
    """
    customers = Customer.query.all()
    return jsonify([{'id': cust.id, 'name': cust.name, 'email': cust.email, 'phone': cust.phone} for cust in customers]), 200
