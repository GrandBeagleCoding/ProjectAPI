from dbModels import *
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger
from playhouse.shortcuts import model_to_dict
from typing import List, Dict

app = Flask(__name__, static_url_path="/localhost:1810")
api = Api(app)
swagger = Swagger(app)

class HelloWorld(Resource):
    """
    This is the Hello World API
    ---
    tags:
      - hello
    parameters:
      - name: name
        in: query
        type: string
        required: true
        description: The name of the person to greet
    responses:
      200:
        description: A greeting message
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the person to greet')
        args = parser.parse_args()
        name = args['name']
        return {'message': f'Hello, {name}!'}

api.add_resource(HelloWorld, '/hello')

# Get-Calls
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id):
    try:
        employee = Employee.get(Employee.id == id)
        return jsonify(model_to_dict(employee))
    except Employee.DoesNotExist:
        return jsonify({'error': 'Employee not found'}), 404

@app.route('/departments/<int:id>', methods=['GET'])
def get_department_by_id(id):
    try:
        department = Department.get(Department.id == id)
        return jsonify(model_to_dict(department))
    except Department.DoesNotExist:
        return jsonify({'error': 'Department not found'}), 404

@app.route('/departments/<int:id>', methods=['GET'])
def get_request_by_id(id):
    try:
        leaverequest = Leaverequest.get(Leaverequest.id == id)
        return jsonify(model_to_dict(leaverequest))
    except Department.DoesNotExist:
        return jsonify({'error': 'Department not found'}), 404

@app.route('/employees/all', methods=['GET'])
def get_all_employees():
    try:
        employees = [model_to_dict(employee) for employee in Employee.select()]
        return jsonify(employees)
    except Employee.DoesNotExist:
        return jsonify({'error': 'Employee not found'})

@app.route('/departments/all', methods=['GET'])
def get_all_departments():
    try:
        departments = [model_to_dict(department) for department in Department.select()]
        return jsonify(departments)
    except Employee.DoesNotExist:
        return jsonify({'error': 'Employee not found'})

@app.route('/leaverequests/all', methods=['GET'])
def get_all_leaverequests():
    try:
        leaverequests = [model_to_dict(leaverequest) for leaverequest in Leaverequest.select()]
        return jsonify(leaverequests)
    except Employee.DoesNotExist:
        return jsonify({'error': 'Employee not found'})

# POST calls
@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    employee = Employee.create(**data)
    return jsonify(model_to_dict(employee)), 201

@app.route('/departments', methods=['POST'])
def create_department():
    data = request.json
    department = Department.create(**data)
    return jsonify(model_to_dict(department)), 201

@app.route('/leave_requests', methods=['POST'])
def create_leave_request():
    data = request.json
    leaverequest = Leaverequest.create(**data)
    return jsonify(model_to_dict(leaverequest)), 201


if __name__ == '__main__':

    database.connect(reuse_if_open=True)

    app.run(host='localhost', port='1810')

    database.close()

