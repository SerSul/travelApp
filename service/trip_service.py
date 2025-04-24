from datetime import datetime
from typing import Dict, Optional
from entity.models import db, BusinessTrip, Employee
from entity.enums import TripStatus, TripType
from sqlalchemy.exc import SQLAlchemyError

class TripService:
    def create_trip(self, trip_data: Dict) -> Optional[Dict]:
        try:
            # Проверяем существование сотрудника
            employee = Employee.query.get(trip_data['employee_id'])
            if not employee:
                raise ValueError("Employee not found")

            # Создаем командировку
            trip = BusinessTrip(
                destination=trip_data['destination'],
                purpose=trip_data['purpose'],
                start_date=datetime.strptime(trip_data['start_date'], '%Y-%m-%d').date(),
                end_date=datetime.strptime(trip_data['end_date'], '%Y-%m-%d').date(),
                budget=trip_data.get('budget'),
                trip_type=TripType(trip_data['trip_type']) if 'trip_type' in trip_data else None,
                status=TripStatus(trip_data['status']) if 'status' in trip_data else TripStatus.PLANNED,
                employee_id=employee.id
            )
            db.session.add(trip)
            db.session.commit()

            return self._format_trip_response(trip)

        except ValueError as e:
            db.session.rollback()
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception("Database error")
        except Exception as e:
            db.session.rollback()
            raise

    def delete_trip(self, trip_id: int) -> bool:
        try:
            trip = BusinessTrip.query.get(trip_id)
            if not trip:
                return False

            db.session.delete(trip)
            db.session.commit()
            return True

        except SQLAlchemyError:
            db.session.rollback()
            raise Exception("Database error")

    def get_trips_by_employee_id(self, employee_id: int) -> list:
        try:
            trips = BusinessTrip.query.filter_by(employee_id=employee_id).all()
            return [self._format_trip_response(trip) for trip in trips]
        except SQLAlchemyError as e:
            raise Exception("Database error")
        except Exception as e:
            raise

    def _format_trip_response(self, trip: BusinessTrip) -> Dict:
        return {
            "id": trip.id,
            "destination": trip.destination,
            "purpose": trip.purpose,
            "start_date": trip.start_date.isoformat(),
            "end_date": trip.end_date.isoformat(),
            "status": trip.status.name,
            "employee_id": trip.employee_id,
        }

