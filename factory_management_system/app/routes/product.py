from flask import Blueprint, request, jsonify
from app.models import db, Product
from flask_limiter import Limiter

bp = Blueprint('product', __name__)
limiter = Limiter()

@bp.route('/products', methods=['POST'])
@limiter.limit("10 per minute")
def create_product():
    """Create a new product."""
    data = request.json
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'id': new_product.id, 'name': new_product.name, 'price': new_product.price}), 201

@bp.route('/products', methods=['GET'])
def get_products():
    """Get all products."""
    products = Product.query.all()
    return jsonify([{'id': prod.id, 'name': prod.name, 'price': prod.price} for prod in products]), 200
