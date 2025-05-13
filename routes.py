from flask import request

from service.trip_service import TripService
from swagger_models import *
from service.employee_service import EmployeeService
from config import ns, require_api_key

employee_service = EmployeeService()

@ns.route('/')
class EmployeeList(Resource):
    @ns.marshal_list_with(employee_response_model)
    @require_api_key
    @ns.doc(security='apikey')
    def get(self):
        """Получить список всех сотрудников"""
        return employee_service.get_all_employees()

    @ns.expect(employee_create_model)
    @ns.marshal_with(employee_response_model, code=201)
    @require_api_key
    @ns.doc(security='apikey')
    def post(self):
        """Создать нового сотрудника"""
        data = request.get_json()
        return employee_service.create_employee(data), 201


@ns.route('/<int:employee_id>')
@ns.param('employee_id', 'ID сотрудника')
class EmployeeById(Resource):
    @ns.marshal_with(employee_response_model)
    @require_api_key
    @ns.doc(security='apikey')
    def get(self, employee_id):
        """Получить информацию о сотруднике по ID"""
        employee = employee_service.get_employee_by_id(employee_id)
        if employee:
            return employee
        ns.abort(404, 'Сотрудник не найден')

    @require_api_key
    @ns.doc(security='apikey')
    def delete(self, employee_id):
        """Деактивировать сотрудника"""
        employee_service.deactivate_employee(employee_id)
        return '', 204

trip_service = TripService()

@ns.route('/trips')
class TripList(Resource):
    @ns.marshal_list_with(trip_response_model)
    @require_api_key
    @ns.doc(security='apikey')
    def get(self):
        """Получить список всех командировок"""
        trips = trip_service.get_all_trips()
        return trips

    @ns.expect(trip_create_model)
    @ns.marshal_with(trip_response_model, code=201)
    @require_api_key
    @ns.doc(security='apikey')
    def post(self):
        """Создать новую командировку"""
        data = request.get_json()
        return trip_service.create_trip(data), 201


@ns.route('/trips/<int:trip_id>')
@ns.param('trip_id', 'ID командировки')
class TripById(Resource):
    @ns.marshal_with(trip_response_model)
    @require_api_key
    @ns.doc(security='apikey')
    def get(self, trip_id):
        """Получить информацию о командировке по ID"""
        trip = trip_service.get_trip_by_id(trip_id)
        if trip:
            return trip
        ns.abort(404, 'Командировка не найдена')

    @require_api_key
    @ns.doc(security='apikey')
    def delete(self, trip_id):
        """Удалить командировку"""
        success = trip_service.delete_trip(trip_id)
        if success:
            return '', 204
        else:
            ns.abort(404, 'Командировка не найдена')

@ns.route('/employee/<int:employee_id>/trips')
@ns.param('employee_id', 'ID сотрудника')
class TripByEmployee(Resource):
    @ns.marshal_list_with(trip_response_model)
    @require_api_key
    @ns.doc(security='apikey')
    def get(self, employee_id):
        """Получить все командировки для сотрудника по его ID"""
        trips = trip_service.get_trips_by_employee_id(employee_id)
        if trips:
            return trips
        ns.abort(404, 'Командировки для сотрудника не найдены')