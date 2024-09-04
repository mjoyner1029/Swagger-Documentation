from flask import Blueprint, request
from flask_restplus import Api, Resource, fields
from app.models import db, Product

bp = Blueprint('products', __name__)
api = Api(bp, doc='/docs')

product_model = api.model('Product', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a product'),
    'name': fields.String(required=True, description='The name of the product'),
    'price': fields.Float(required=True, description='The price of the product')
})

@api.route('/')
class ProductList(Resource):
    @api.doc('create_product')
    @api.expect(product_model)
    @api.marshal_with(product_model, code=201)
    @api.response(400, 'Invalid input', error_model)
    @api.response(500, 'Server error', error_model)
    def post(self):
        """Create a new product"""
        data = request.json
        if not data:
            api.abort(400, 'Invalid input', errors={'message': 'Request body missing'})
        new_product = Product(name=data['name'], price=data['price'])
        db.session.add(new_product)
        db.session.commit()
        return new_product, 201

    @api.doc('list_products')
    @api.marshal_list_with(product_model)
    def get(self):
        """List all products"""
        products = Product.query.all()
        return products
