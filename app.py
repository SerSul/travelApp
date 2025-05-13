from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate

from entity import db
from routes import ns as main_namespace

app = Flask(__name__)
app.config.from_object('config.Config')

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}


# Создаем объект API
api = Api(app, version='1.0', title='Employee API', description='Управление сотрудниками и командировками', authorizations=authorizations,
    security='apikey')


# Подключаем namespace
api.add_namespace(main_namespace, path='/api')

# Инициализируем миграции и БД
migrate = Migrate(app, db)
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
