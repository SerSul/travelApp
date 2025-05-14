from entity import *
from sqlalchemy import Index

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

Index('idx_employee_personal_data', Employee.personal_data_id)
