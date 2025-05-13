from entity import *
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Index
from entity.enums import *

class BusinessTrip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(200), nullable=False)
    purpose = db.Column(db.String(500), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=True)
    trip_type = db.Column(SQLAlchemyEnum(TripType), nullable=True)
    status = db.Column(SQLAlchemyEnum(TripStatus), default=TripStatus.PLANNED)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

    def __repr__(self):
        return f"<BusinessTrip to {self.destination}>"

Index('idx_business_trip_employee', BusinessTrip.employee_id)