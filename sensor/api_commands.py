from hashlib import new
import json
from urllib.error import HTTPError
from flask import request
from flask_restful import Resource
from uuid import uuid1
import boto3
from botocore.exceptions import ClientError
import requests


sendQueueUrl='https://sqs.us-east-1.amazonaws.com/804352613378/MisoQueue'
sqs_client =boto3.client('sqs', region_name='us-east-1',
                                aws_access_key_id="AKIA3WRZG3QBCY3A7T6R",
                                aws_secret_access_key="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")


class signal:
  def __init__(id, signal_type, signal_message):
    id=id,
    signal_type = signal_type
    signal_message = signal_message


class SensorResource(Resource):
    def post(self):
        uuid_trans =uuid1()
        new_signal = signal(
            id = uuid_trans,
            signal_type=request.json['signal_type'],
            signal_message=request.json['signal_message'],
        )
        send_queue_message(new_signal)
        response_notification = requests.post(f"http://127.0.0.1:5000/postSignals", json={"id": str(new_signal.id) , "signal_type": str(new_signal.signal_type) , "signal_message":str(new_signal.signal_message) }, headers={"Content-Type":"application/json"})
        print(response_notification)
       
        if response_notification.ok:
            print(response_notification.json())
        else :
            print('error al estabelcer conexión con servicio monitor  status_code ', response_notification.status_code )
    



def send_queue_message(new_signal) :
    try:
        messageBody = {
            "id":str(new_signal.id),
            "signal_type":str(new_signal.signal_type),
            "signal_message": str(new_signal.signal_message)
        }
      

        response = sqs_client.send_message(QueueUrl=sendQueueUrl,
                                            MessageBody = json.dumps(messageBody),
                                            MessageAttributes = {
                                                'id' :{ 'DataType': 'String',
                                                        'StringValue': str(new_signal.id)
                                                }})
    except ClientError:
        raise
    else:
        return response

