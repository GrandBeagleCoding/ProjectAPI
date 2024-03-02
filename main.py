from dbModels import *
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger
from playhouse.shortcuts import model_to_dict

app = Flask(__name__)
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
    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the person to greet')
        args = parser.parse_args()
        name = args['name']
        return {'message': f'Hello, {name}!'}

api.add_resource(HelloWorld, '/hello')

# Get-Calls
@app.route('/employees/all', methods=['GET'])
def get_all_employees():
    try:
        employees = [model_to_dict(employee) for employee in Employee.select()]
        return jsonify(employees)
    except Employee.DoesNotExist:
        return jsonify({'error': 'Employees not found'}), 404

@app.route('/departments/<int:id>/employees', methods=['GET'])
def get_all_employees_of_dept(id):
    try:
        employees_of_dept = [model_to_dict(employee) for employee in Employee.select().where(Employee.department_id == id)]
        return jsonify(employees_of_dept)
    except Employee.DoesNotExist:
        return jsonify({'error': 'Employees not found'}), 404

@app.route('/departments/all', methods=['GET'])
def get_all_departments():
    try:
        departments = [model_to_dict(department) for department in Department.select()]
        return jsonify(departments)
    except Department.DoesNotExist:
        return jsonify({'error': 'Departments not found'}), 404

@app.route('/leaverequests/all', methods=['GET'])
def get_all_leaverequests():
    try:
        leaverequests = [model_to_dict(leaverequest) for leaverequest in Leaverequest.select()]
        return jsonify(leaverequests)
    except Leaverequest.DoesNotExist:
        return jsonify({'error': 'Leaverequests not found'}), 404

@app.route('/leaverequests/employee/<int:id>', methods=['GET'])
def get_all_requests_of_employee(id):
    try:
        requests_of_employeeid = [model_to_dict(leaverequest) for leaverequest in Leaverequest.select().where(Leaverequest.employee_id == id)]
        return jsonify(requests_of_employeeid)
    except:
        return jsonify(Exception)

# POST calls
@app.route('/employees/add/', methods=['POST'])
def create_employee():
    data = request.json
    employee = Employee.create(**data)
    return jsonify(model_to_dict(employee)), 201

@app.route('/departments/add/', methods=['POST'])
def create_department():
    data = request.json
    department = Department.create(**data)
    return jsonify(model_to_dict(department)), 201

@app.route('/leave_requests/update/<int:id>', methods=['PUT'])
def update_request(id):
    row = Leaverequest.get(Leaverequest.request_id == id)
    row.status = request.json["status"]
    row.save()
    return jsonify({'Success': 'Yes'}), 201


if __name__ == '__main__':

    database.connect(reuse_if_open=True)

    app.run(host='localhost', port=1810)

    database.close()
