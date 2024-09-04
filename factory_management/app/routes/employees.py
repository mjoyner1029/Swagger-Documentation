from flask import Blueprint, request
from flask_restplus import Api, Resource, fields
from app.models import db, Employee

bp = Blueprint('employees', __name__)
api = Api(bp, doc='/docs')

employee_model = api.model('Employee', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an employee'),
    'name': fields.String(required=True, description='The name of the employee'),
    'position': fields.String(required=True, description='The position of the employee')
})

error_model = api.model('Error', {
    'message': fields.String(description='Error message'),
    'code': fields.Integer(description='Error code')
})

@api.route('/')
class EmployeeList(Resource):
    @api.doc('create_employee')
    @api.expect(employee_model)
    @api.marshal_with(employee_model, code=201)
    @api.response(400, 'Invalid input', error_model)
    @api.response(500, 'Server error', error_model)
    def post(self):
        """Create a new employee"""
        data = request.json
        if not data:
            api.abort(400, 'Invalid input', errors={'message': 'Request body missing'})
        new_employee = Employee(name=data['name'], position=data['position'])
        db.session.add(new_employee)
        db.session.commit()
        return new_employee, 201

    @api.doc('list_employees')
    @api.marshal_list_with(employee_model)
    def get(self):
        """List all employees"""
        employees = Employee.query.all()
        return employees
