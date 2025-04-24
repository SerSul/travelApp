from flask import Blueprint, request, jsonify
from service.employee_service import EmployeeService
from service.trip_service import TripService

api = Blueprint('api', __name__)
employee_service = EmployeeService()
trip_service = TripService()

@api.route('/employees', methods=['POST'])
def create_employee():
    try:
        data = request.get_json()
        result = employee_service.create_employee(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@api.route('/trips', methods=['POST'])
def create_trip():
    try:
        data = request.get_json()
        result = trip_service.create_trip(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/trips/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    try:
        if trip_service.delete_trip(trip_id):
            return jsonify({"message": "Trip deleted successfully"}), 200
        return jsonify({"error": "Trip not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/employees', methods=['GET'])
def get_employees():
    try:
        employees = employee_service.get_all_employees()
        return jsonify(employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    try:
        employee = employee_service.get_employee_by_id(employee_id)
        if employee:
            return jsonify(employee), 200
        return jsonify({"error": "Employee not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/employees/<int:employee_id>/trips', methods=['GET'])
def get_employee_trips(employee_id):
    try:
        trips = trip_service.get_trips_by_employee_id(employee_id)
        return jsonify(trips), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500