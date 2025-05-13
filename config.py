import os
from flask_restx import Namespace
from functools import wraps
from flask import request, abort

ns = Namespace('employees', description='Операции с сотрудниками')

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        provided_key = request.headers.get('X-API-KEY')  # Получаем ключ из заголовков
        if not provided_key or provided_key != API_KEY:  # Проверяем на совпадение с API_KEY
            abort(401, 'Unauthorized: Invalid or missing API key')  # Если ключ не совпадает — ошибка
        return func(*args, **kwargs)  # Если все верно, вызываем основной метод
    return wrapper


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:123@localhost:5432/travel_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
