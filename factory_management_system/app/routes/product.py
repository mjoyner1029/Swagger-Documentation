from flask import Blueprint, request, jsonify
from app.models import db, Product

bp = Blueprint('product', __name__)

@bp.route('/products', methods=['POST'])
@limiter.limit("10 per minute")
def create_product():
    """Create a new product.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Product
          properties:
            name:
              type: string
              example: "Widget"
            price:
              type: number
              format: float
              example: 19.99
    responses:
      201:
        description: Product created successfully
        schema:
          id: ProductResponse
          properties:
            id:
              type: integer
            name:
              type: string
            price:
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
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'id': new_product.id}), 201

@bp.route('/products', methods=['GET'])
def get_products():
    """Get all products.
    ---
    responses:
      200:
        description: A list of products
        schema:
          type: array
          items:
            id: Product
            properties:
              id:
                type: integer
              name:
                type: string
              price:
                type: number
                format: float
    """
    products = Product.query.all()
    return jsonify([{'id': prod.id, 'name': prod.name, 'price': prod.price} for prod in products]), 200
