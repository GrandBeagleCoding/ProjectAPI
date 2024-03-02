import unittest
import requests
import json

class TestEmployeeAPI(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost:1810'

    def test_get_all_employees(self):
        response = requests.get(f'{self.url}/employees/all')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(len(data), 0)

    def test_get_all_employees_of_dept(self):
        response = requests.get(f'{self.url}/departments/1/employees')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(len(data), 0)


    def test_create_employee(self):

        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'department_id': 1
        }
        response = requests.post(f'{self.url}/employees/add/', json=data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.text)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'johndoe@example.com')
        self.assertEqual(data['department_id'], 1)


class TestDepartmentAPI(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:1810'


    def test_get_all_departments(self):
        response = requests.get(f'{self.url}/departments/all')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(len(data), 0)


    def test_create_department(self):
        data = {
            'department_name': 'testdgtfs'
        }
        response = requests.post(f'{self.url}/departments/add/', json=data)
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.text)
        self.assertEqual(data['department_name'], 'testdgtfs')


class TestLeaveRequestAPI(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:1810'

    def test_get_all_leave_requests(self):
        response = requests.get(f'{self.url}/leaverequests/all')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(len(data), 0)

    def test_get_all_leave_requests_of_employee(self):
        response = requests.get(f'{self.url}/leaverequests/employee/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(len(data), 0)

    def test_update_leave_request(self):
        data = {
            'status': '2'
        }
        response = requests.put(f'{self.url}/leave_requests/update/2', json=data)
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
