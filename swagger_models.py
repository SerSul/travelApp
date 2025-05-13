from flask_restx import Namespace, Resource, fields
from config import ns
# --- Swagger Models ---

personal_data_model = ns.model('PersonalData', {
    'first_name': fields.String(required=True, description='Имя'),
    'last_name': fields.String(required=True, description='Фамилия'),
    'middle_name': fields.String(required=False, description='Отчество'),
    'date_of_birth': fields.String(required=True, description='Дата рождения (YYYY-MM-DD)')
})

contact_info_model = ns.model('ContactInfo', {
    'phone': fields.String(required=True, description='Телефон'),
    'email': fields.String(required=True, description='Email'),
    'work_phone': fields.String(required=False, description='Рабочий телефон'),
    'emergency_contact': fields.String(required=False, description='Экстренный контакт'),
    'emergency_phone': fields.String(required=False, description='Телефон экстренного контакта')
})

passport_data_model = ns.model('PassportData', {
    'passport_type': fields.String(required=True, description='Тип паспорта', enum=['INTERNAL', 'FOREIGN']),
    'passport_number': fields.String(required=True, description='Номер паспорта'),
    'issued_by': fields.String(required=True, description='Кем выдан'),
    'issue_date': fields.String(required=True, description='Дата выдачи (YYYY-MM-DD)'),
    'expiry_date': fields.String(required=False, description='Дата окончания действия'),
    'birth_place': fields.String(required=False, description='Место рождения')
})

employee_create_model = ns.model('EmployeeCreate', {
    'position': fields.String(required=False, description='Должность'),
    'personal_data': fields.Nested(personal_data_model, required=True),
    'contact_info': fields.Nested(contact_info_model, required=True),
    'passport_data': fields.Nested(passport_data_model, required=False)
})

employee_response_model = ns.model('EmployeeResponse', {
    'id': fields.Integer(description='ID сотрудника'),
    'position': fields.String(description='Должность'),
    'full_name': fields.String(description='ФИО'),
    'email': fields.String(description='Email'),
    'passport': fields.String(description='Номер паспорта')
})