from flask import Blueprint, request, jsonify
from app.models import db, Employee

bp = Blueprint('employee', __name__)

@bp.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    employee = Employee(name=data['name'], position=data['position'])
    db.session.add(employee)
    db.session.commit()
    return jsonify({'id': employee.id, 'name': employee.name, 'position': employee.position}), 201

@bp.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{'id': emp.id, 'name': emp.name, 'position': emp.position} for emp in employees]), 200
