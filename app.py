from flask import Flask, jsonify, request
from models import db, Employee, BusinessTrip
from datetime import date
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object('config.Config')

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{
        'id': employee.id,
        'full_name': employee.full_name,
        'position': employee.position,
        'trips': [{
            'destination': trip.destination,
            'start_date': trip.start_date.isoformat(),
            'end_date': trip.end_date.isoformat()
        } for trip in employee.trips]
    } for employee in employees])

# Получение сотрудника по id
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify({
        'id': employee.id,
        'full_name': employee.full_name,
        'position': employee.position,
        'trips': [{
            'destination': trip.destination,
            'start_date': trip.start_date.isoformat(),
            'end_date': trip.end_date.isoformat()
        } for trip in employee.trips]
    })

# Добавление нового сотрудника
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    new_employee = Employee(
        full_name=data['full_name'],
        position=data.get('position')
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'id': new_employee.id, 'full_name': new_employee.full_name, 'position': new_employee.position}), 201

# Добавление командировки
@app.route('/business_trips', methods=['POST'])
def add_business_trip():
    data = request.get_json()
    new_trip = BusinessTrip(
        destination=data['destination'],
        start_date=date.fromisoformat(data['start_date']),
        end_date=date.fromisoformat(data['end_date']),
        employee_id=data['employee_id']
    )
    db.session.add(new_trip)
    db.session.commit()
    return jsonify({
        'id': new_trip.id,
        'destination': new_trip.destination,
        'start_date': new_trip.start_date.isoformat(),
        'end_date': new_trip.end_date.isoformat(),
        'employee_id': new_trip.employee_id
    }), 201

if __name__ == '__main__':
    app.run(debug=True)
