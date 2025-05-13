from flask import request
from swagger_models import *
from service.employee_service import EmployeeService
from config import ns

employee_service = EmployeeService()

@ns.route('/')
class EmployeeList(Resource):
    @ns.marshal_list_with(employee_response_model)
    def get(self):
        """Получить список всех сотрудников"""
        return employee_service.get_all_employees()

    @ns.expect(employee_create_model)
    @ns.marshal_with(employee_response_model, code=201)
    def post(self):
        """Создать нового сотрудника"""
        data = request.get_json()
        return employee_service.create_employee(data), 201


@ns.route('/<int:employee_id>')
@ns.param('employee_id', 'ID сотрудника')
class EmployeeById(Resource):
    @ns.marshal_with(employee_response_model)
    def get(self, employee_id):
        """Получить информацию о сотруднике по ID"""
        employee = employee_service.get_employee_by_id(employee_id)
        if employee:
            return employee
        ns.abort(404, 'Сотрудник не найден')

    def delete(self, employee_id):
        """Деактивировать сотрудника"""
        employee_service.deactivate_employee(employee_id)
        return '', 204
