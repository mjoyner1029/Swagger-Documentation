from flask import Blueprint, request, jsonify
from app.models import db, Employee

bp = Blueprint('employee', __name__)

@bp.route('/employees', methods=['POST'])
@limiter.limit("10 per minute")
def create_employee():
    """Create a new employee.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Employee
          properties:
            name:
              type: string
              example: "John Doe"
            position:
              type: string
              example: "Engineer"
    responses:
      201:
        description: Employee created successfully
        schema:
          id: EmployeeResponse
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "John Doe"
            position:
              type: string
              example: "Engineer"
      400:
        description: Invalid input
        schema:
          id: ErrorResponse
          properties:
            error:
              type: string
              example: "Invalid data"
            message:
              type: string
              example: "Position cannot be empty."
      500:
        description: Server error
        schema:
          id: ErrorResponse
          properties:
            error:
              type: string
              example: "Server Error"
            message:
              type: string
              example: "An unexpected error occurred."
    """
    data = request.json
    new_employee = Employee(name=data['name'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'id': new_employee.id, 'name': new_employee.name, 'position': new_employee.position}), 201

@bp.route('/employees', methods=['GET'])
def get_employees():
    """Get all employees.
    ---
    responses:
      200:
        description: A list of employees
        schema:
          type: array
          items:
            id: Employee
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "John Doe"
              position:
                type: string
                example: "Engineer"
    """
    employees = Employee.query.all()
    return jsonify([{'id': emp.id, 'name': emp.name, 'position': emp.position} for emp in employees]), 200
