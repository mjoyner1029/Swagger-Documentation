from flask import Blueprint, request, jsonify
from app.models import db, Production

bp = Blueprint('production', __name__)

@bp.route('/production', methods=['POST'])
def create_production():
    data = request.json
    production = Production(product_id=data['product_id'], quantity_produced=data['quantity_produced'], date_produced=data['date_produced'])
    db.session.add(production)
    db.session.commit()
    return jsonify({'id': production.id, 'product_id': production.product_id, 'quantity_produced': production.quantity_produced, 'date_produced': production.date_produced}), 201

@bp.route('/production', methods=['GET'])
def get_production():
    production_records = Production.query.all()
    return jsonify([{'id': prod.id, 'product_id': prod.product_id, 'quantity_produced': prod.quantity_produced, 'date_produced': prod.date_produced} for prod in production_records]), 200
