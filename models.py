from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    employee = db.relationship('Employee', backref='user', uselist=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    employees = db.relationship('Employee', backref='department', lazy=True)

    def __repr__(self):
        return f"<Department {self.name}>"


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)

    trips = db.relationship('BusinessTrip', backref='employee', lazy=True)

    def __repr__(self):
        return f"<Employee {self.full_name}>"


class BusinessTrip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

    def __repr__(self):
        return f"<BusinessTrip {self.destination}>"
