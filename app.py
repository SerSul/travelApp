from flask import Flask, jsonify, request
from entity.models import db, Employee, BusinessTrip
from datetime import date
from flask_migrate import Migrate
from routes import api as blueprint


app = Flask(__name__)
app.config.from_object('config.Config')
app.register_blueprint(blueprint.api, url_prefix='/api')

migrate = Migrate(app, db)
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
