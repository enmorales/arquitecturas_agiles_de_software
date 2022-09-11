from hashlib import new
import json
from re import S
from flask import request
from flask_restful import Resource
from modelos import db, signal, SignalSchema

signal_schema = SignalSchema()
signals_schema = SignalSchema(many = True)

class postMessages(Resource):
    def post(self):
        new_signal = signal(
            id = request.json['id'],
            signal_type=request.json['signal_type'],
            signal_message=request.json['signal_message'],
       )
        db.session.add(new_signal)
        db.session.commit()
        return signal_schema.dump(new_signal)



def postJson(datos):
      datos_dict = json.loads(datos)
      print('asi se ve uno', datos_dict['id'])
      new_signal = signal(
                id = datos_dict['id'],
                signal_type=datos_dict['signal_type'],
                signal_message=datos_dict['signal_message'],
        )
      db.session.add(new_signal)
      db.session.commit()
      return signal_schema.dump(new_signal)