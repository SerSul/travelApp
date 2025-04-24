# schemas.py
from marshmallow import Schema, fields, validate


class PersonalDataSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    middle_name = fields.Str(validate=validate.Length(max=100))
    date_of_birth = fields.Date(required=True)
    gender = fields.Str(validate=validate.Length(max=10))
    nationality = fields.Str(validate=validate.Length(max=100))
    tax_id = fields.Str(validate=validate.Length(max=50))
    insurance_number = fields.Str(validate=validate.Length(max=50))


class EmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    position = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    hire_date = fields.Date(required=True)
    termination_date = fields.Date()
    salary = fields.Float()
    email = fields.Email(required=True)
    work_phone = fields.Str(validate=validate.Length(max=20))
    active = fields.Boolean()
    department_id = fields.Int(required=True)
    personal_data_id = fields.Int(required=True)

    # Вложенная схема для связанных данных
    personal_data = fields.Nested(PersonalDataSchema, dump_only=True)
