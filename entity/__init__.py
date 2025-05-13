from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from entity import enums

from entity.enums import *


# Импорт моделей
from .BusinessTrip import BusinessTrip
from .ContactInfo import ContactInfo
from .Employee import Employee
from .PassportData import PassportData
from .PersonalData import PersonalData
from .enums import *

__all__ = ['db', 'BusinessTrip', 'Employee', 'PassportData', 'PersonalData', 'ContactInfo', 'enums']

