
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from uuid import uuid4

from api_commands import SensorResource

app = Flask(__name__)
app_context = app.app_context()
app_context.push()
ma = Marshmallow(app)

api = Api(app)

api.add_resource(SensorResource , '/signals')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)