from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Index

from entity.enums import *

db = SQLAlchemy()

class PassportData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    passport_type = db.Column(SQLAlchemyEnum(PassportType), nullable=False, default=PassportType.INTERNAL)
    passport_number = db.Column(db.String(50), nullable=False, index=True)
    issued_by = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=True)
    birth_place = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Passport {self.passport_number}>"

class ContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    work_phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    emergency_contact = db.Column(db.String(100), nullable=True)
    emergency_phone = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"<ContactInfo {self.email}>"

class PersonalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<PersonalData {self.first_name} {self.last_name}>"

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    personal_data_id = db.Column(db.Integer, db.ForeignKey('personal_data.id'), nullable=True)
    personal_data = db.relationship('PersonalData', backref='employees', uselist=False)

    passport = db.relationship('PassportData', backref='employee_owner', uselist=False, cascade="all, delete-orphan")
    contact_info = db.relationship('ContactInfo', backref='employee_owner', uselist=False, cascade="all, delete-orphan")
    trips = db.relationship('BusinessTrip', backref='employee', lazy=True, cascade="all, delete-orphan")

    @property
    def full_name(self):
        if self.personal_data:
            return f"{self.personal_data.last_name} {self.personal_data.first_name}"
        return "Unknown"

    def __repr__(self):
        return f"<Employee {self.full_name}>"

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

Index('idx_employee_personal_data', Employee.personal_data_id)
Index('idx_business_trip_employee', BusinessTrip.employee_id)