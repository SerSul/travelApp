from entity import *


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