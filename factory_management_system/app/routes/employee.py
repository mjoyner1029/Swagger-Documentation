from flask import Blueprint, request, jsonify
from app.models import db, Employee
from flask_limiter import Limiter

bp = Blueprint('employee', __name__)
limiter = Limiter()

@bp.route('/employees', methods=['POST'])
@limiter.limit("10 per minute")
def create_employee():
    """Create a new employee."""
    data = request.json
    new_employee = Employee(name=data['name'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'id': new_employee.id, 'name': new_employee.name, 'position': new_employee.position}), 201

@bp.route('/employees', methods=['GET'])
def get_employees():
    """Get all employees."""
    employees = Employee.query.all()
    return jsonify([{'id': emp.id, 'name': emp.name, 'position': emp.position} for emp in employees]), 200
