from flask import Blueprint, request, jsonify
from app.models import db, Product

bp = Blueprint('product', __name__)

@bp.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product = Product(name=data['name'], price=data['price'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price}), 201

@bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': prod.id, 'name': prod.name, 'price': prod.price} for prod in products]), 200
