from datetime import datetime
from typing import Dict, Optional
from entity import db, Employee, PassportData, ContactInfo, PersonalData
from entity.enums import PassportType
from sqlalchemy.exc import SQLAlchemyError


class EmployeeService:
    def create_employee(self, employee_data: Dict) -> Optional[Dict]:
        try:
            if not all(key in employee_data for key in ['personal_data', 'contact_info']):
                raise ValueError("Missing required fields")

            # Создание персональных данных
            personal_data = self._create_personal_data(employee_data['personal_data'])

            # Создание сотрудника
            employee = Employee(
                position=employee_data.get('position'),
                personal_data_id=personal_data.id
            )
            db.session.add(employee)
            db.session.flush()

            # Создание контактов
            contact_info = self._create_contact_info(employee.id, employee_data['contact_info'])

            # Создание паспорта (если есть данные)
            passport_data = None
            if 'passport_data' in employee_data:
                passport_data = self._create_passport_data(employee.id, employee_data['passport_data'])

            db.session.commit()

            return self._format_employee_response(employee, personal_data, contact_info, passport_data)

        except ValueError as e:
            db.session.rollback()
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception("Database error: " + e.args[0])
        except Exception as e:
            db.session.rollback()
            raise

    def deactivate_employee(self, employee_id: int) -> None:
        try:
            employee = Employee.query.get(employee_id)
            employee.is_active = False
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception("Database error")
        except Exception as e:
            db.session.rollback()
            raise

    def get_all_employees(self) -> list:
        try:
            employees = Employee.query.filter_by(active=True).all()
            return [self._format_employee_response(
                emp,
                emp.personal_data,
                emp.contact_info,
                emp.passport
            ) for emp in employees]
        except SQLAlchemyError as e:
            raise Exception("Database error")
        except Exception as e:
            raise

    def get_employee_by_id(self, employee_id: int) -> Optional[Dict]:
        try:
            employee = Employee.query.get(employee_id)
            if not employee or not employee.active:
                return None

            return self._format_employee_response(
                employee,
                employee.personal_data,
                employee.contact_info,
                employee.passport
            )
        except SQLAlchemyError as e:
            raise Exception("Database error")
        except Exception as e:
            raise

    def _create_personal_data(self, data: Dict) -> PersonalData:
        personal_data = PersonalData(
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data.get('middle_name', ''),
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        )
        db.session.add(personal_data)
        db.session.flush()
        return personal_data

    def _create_contact_info(self, employee_id: int, data: Dict) -> ContactInfo:
        contact_info = ContactInfo(
            employee_id=employee_id,
            phone=data['phone'],
            email=data['email'],
            work_phone=data.get('work_phone'),
            emergency_contact=data.get('emergency_contact'),
            emergency_phone=data.get('emergency_phone')
        )
        db.session.add(contact_info)
        return contact_info

    def _create_passport_data(self, employee_id: int, data: Dict) -> PassportData:
        passport_data = PassportData(
            employee_id=employee_id,
            passport_type=PassportType(data['passport_type']),
            passport_number=data['passport_number'],
            issued_by=data['issued_by'],
            issue_date=datetime.strptime(data['issue_date'], '%Y-%m-%d').date(),
            expiry_date=datetime.strptime(data['expiry_date'], '%Y-%m-%d').date() if data.get('expiry_date') else None,
            birth_place=data.get('birth_place')
        )
        db.session.add(passport_data)
        return passport_data

    def _format_employee_response(self, employee: Employee, personal_data: PersonalData,
                                  contact_info: ContactInfo, passport_data: Optional[PassportData]) -> Dict:
        return {
            "id": employee.id,
            "position": employee.position,
            "full_name": f"{personal_data.last_name} {personal_data.first_name}",
            "email": contact_info.email,
            "passport": passport_data.passport_number if passport_data else None
        }

