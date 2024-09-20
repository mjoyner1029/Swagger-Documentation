from flask import Blueprint, request, jsonify
from app.models import db, Order

bp = Blueprint('order', __name__)

@bp.route('/orders', methods=['POST'])
@limiter.limit("10 per minute")
def create_order():
    """Create a new order.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Order
          properties:
            customer_id:
              type: integer
              example: 1
            product_id:
              type: integer
              example: 1
            quantity:
              type: integer
              example: 3
    responses:
      201:
        description: Order created successfully
        schema:
          id: OrderResponse
          properties:
            id:
              type: integer
            customer_id:
              type: integer
            product_id:
              type: integer
            quantity:
              type: integer
            total_price:
              type: number
              format: float
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
    new_order = Order(customer_id=data['customer_id'], product_id=data['product_id'], quantity=data['quantity'], total_price=0)  # Calculate total price if needed
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'id': new_order.id}), 201

@bp.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders.
    ---
    responses:
      200:
        description: A list of orders
        schema:
          type: array
          items:
            id: Order
            properties:
              id:
                type: integer
              customer_id:
                type: integer
              product_id:
                type: integer
              quantity:
                type: integer
    """
    orders = Order.query.all()
    return jsonify([{'id': ord.id, 'customer_id': ord.customer_id, 'product_id': ord.product_id, 'quantity': ord.quantity} for ord in orders]), 200
