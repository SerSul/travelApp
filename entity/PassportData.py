from entity import *
from sqlalchemy import Enum as SQLAlchemyEnum
from entity.enums import *

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