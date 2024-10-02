from flask import Blueprint, request, jsonify
from app.models import db, Production
from flask_limiter import Limiter

bp = Blueprint('production', __name__)
limiter = Limiter()

@bp.route('/production', methods=['POST'])
@limiter.limit("10 per minute")
def create_production():
    """Record a new production."""
    data = request.json
    new_production = Production(product_id=data['product_id'], quantity_produced=data['quantity_produced'], date_produced=data['date_produced'])
    db.session.add(new_production)
    db.session.commit()
    return jsonify({'id': new_production.id}), 201

@bp.route('/production', methods=['GET'])
def get_production():
    """Get all production records."""
    productions = Production.query.all()
    return jsonify([{'id': prod.id, 'product_id': prod.product_id, 'quantity_produced': prod.quantity_produced, 'date_produced': prod.date_produced.isoformat()} for prod in productions]), 200
