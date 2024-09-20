from flask import Blueprint, request, jsonify
from app.models import db, Production

bp = Blueprint('production', __name__)

@bp.route('/production', methods=['POST'])
@limiter.limit("10 per minute")
def create_production():
    """Record a new production.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Production
          properties:
            product_id:
              type: integer
              example: 1
            quantity_produced:
              type: integer
              example: 100
            date_produced:
              type: string
              format: date
              example: "2024-09-01"
    responses:
      201:
        description: Production recorded successfully
        schema:
          id: ProductionResponse
          properties:
            id:
              type: integer
            product_id:
              type: integer
            quantity_produced:
              type: integer
            date_produced:
              type: string
              format: date
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
    new_production = Production(product_id=data['product_id'], quantity_produced=data['quantity_produced'], date_produced=data['date_produced'])
    db.session.add(new_production)
    db.session.commit()
    return jsonify({'id': new_production.id}), 201

@bp.route('/production', methods=['GET'])
def get_production():
    """Get all production records.
    ---
    responses:
      200:
        description: A list of production records
        schema:
          type: array
          items:
            id: Production
            properties:
              id:
                type: integer
              product_id:
                type: integer
              quantity_produced:
                type: integer
              date_produced:
                type: string
                format: date
    """
    productions = Production.query.all()
    return jsonify([{'id': prod.id, 'product_id': prod.product_id, 'quantity_produced': prod.quantity_produced, 'date_produced': prod.date_produced.isoformat()} for prod in productions]), 200
