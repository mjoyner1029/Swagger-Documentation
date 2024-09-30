from flask import Blueprint, request, jsonify
from app.models import db, Order

bp = Blueprint('order', __name__)

@bp.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order = Order(customer_id=data['customer_id'], product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(order)
    db.session.commit()
    return jsonify({'id': order.id, 'customer_id': order.customer_id, 'product_id': order.product_id, 'quantity': order.quantity}), 201

@bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{'id': ord.id, 'customer_id': ord.customer_id, 'product_id': ord.product_id, 'quantity': ord.quantity} for ord in orders]), 200
