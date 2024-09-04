from flask import Blueprint, request
from flask_restplus import Api, Resource, fields
from app.models import db, Order

bp = Blueprint('orders', __name__)
api = Api(bp, doc='/docs')

order_model = api.model('Order', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an order'),
    'customer_id': fields.Integer(required=True, description='The ID of the customer who placed the order'),
    'product_id': fields.Integer(required=True, description='The ID of the product ordered'),
    'quantity': fields.Integer(required=True, description='The quantity of the product ordered'),
    'total_price': fields.Float(required=True, description='The total price of the order')
})

@api.route('/')
class OrderList(Resource):
    @api.doc('create_order')
    @api.expect(order_model)
    @api.marshal_with(order_model, code=201)
    @api.response(400, 'Invalid input', error_model)
    @api.response(500, 'Server error', error_model)
    def post(self):
        """Create a new order"""
        data = request.json
        if not data:
            api.abort(400, 'Invalid input', errors={'message': 'Request body missing'})
        new_order = Order(
            customer_id=data['customer_id'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            total_price=data['total_price']
        )
        db.session.add(new_order)
        db.session.commit()
        return new_order, 201

    @api.doc('list_orders')
    @api.marshal_list_with(order_model)
    def get(self):
        """List all orders"""
        orders = Order.query.all()
        return orders
