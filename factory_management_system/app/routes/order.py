from flask import Blueprint, request, jsonify
from app.models import db, Order

bp = Blueprint('order', __name__)

@bp.route('/orders', methods=['POST'])
@limiter.limit("10 per minute")
def create_order():
    """Create a new order."""
    data = request.json
    new_order = Order(customer_id=data['customer_id'], product_id=data['product_id'], quantity=data['quantity'], total_price=0)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'id': new_order.id}), 201

@bp.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders."""
    orders = Order.query.all()
    return jsonify([{'id': ord.id, 'customer_id': ord.customer_id, 'product_id': ord.product_id, 'quantity': ord.quantity} for ord in orders]), 200
