from flask import Blueprint, request
from flask_restplus import Api, Resource, fields
from app.models import db, Customer

bp = Blueprint('customers', __name__)
api = Api(bp, doc='/docs')

customer_model = api.model('Customer', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a customer'),
    'name': fields.String(required=True, description='The name of the customer'),
    'email': fields.String(required=True, description='The email of the customer'),
    'phone': fields.String(required=True, description='The phone number of the customer')
})

@api.route('/')
class CustomerList(Resource):
    @api.doc('create_customer')
    @api.expect(customer_model)
    @api.marshal_with(customer_model, code=201)
    @api.response(400, 'Invalid input', error_model)
    @api.response(500, 'Server error', error_model)
    def post(self):
        """Create a new customer"""
        data = request.json
        if not data:
            api.abort(400, 'Invalid input', errors={'message': 'Request body missing'})
        new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
        db.session.add(new_customer)
        db.session.commit()
        return new_customer, 201

    @api.doc('list_customers')
    @api.marshal_list_with(customer_model)
    def get(self):
        """List all customers"""
        customers = Customer.query.all()
        return customers
