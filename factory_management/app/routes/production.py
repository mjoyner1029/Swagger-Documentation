from flask import Blueprint, request
from flask_restplus import Api, Resource, fields
from app.models import db, Production

bp = Blueprint('production', __name__)
api = Api(bp, doc='/docs')

production_model = api.model('Production', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a production record'),
    'product_id': fields.Integer(required=True, description='The ID of the product produced'),
    'quantity_produced': fields.Integer(required=True, description='The quantity of the product produced'),
    'date_produced': fields.Date(required=True, description='The date when the product was produced')
})

@api.route('/')
class ProductionList(Resource):
    @api.doc('create_production')
    @api.expect(production_model)
    @api.marshal_with(production_model, code=201)
    @api.response(400, 'Invalid input', error_model)
    @api.response(500, 'Server error', error_model)
    def post(self):
        """Create a new production record"""
        data = request.json
        if not data:
            api.abort(400, 'Invalid input', errors={'message': 'Request body missing'})
        new_production = Production(
            product_id=data['product_id'],
            quantity_produced=data['quantity_produced'],
            date_produced=data['date_produced']
        )
        db.session.add(new_production)
        db.session.commit()
        return new_production, 201

    @api.doc('list_production')
    @api.marshal_list_with(production_model)
    def get(self):
        """List all production records"""
        productions = Production.query.all()
        return productions
