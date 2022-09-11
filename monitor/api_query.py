from distutils.command.config import config
from email.message import Message
from logging import Logger
from flask_restful import Resource
import json
import boto3
from botocore.config import Config
from modelos import signal , SignalSchema
from botocore.exceptions import ClientError
from api_commands import postMessages,postJson


class receiveMessages(Resource):
    def get(self):
      
        my_config = Config(region_name = 'us-east-1')
        sqs_resource = boto3.resource('sqs', config=my_config ,aws_access_key_id="AKIA3WRZG3QBCY3A7T6R",
                        aws_secret_access_key="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")
        queue = sqs_resource.get_queue_by_name(QueueName="MisoQueue")


        for message in queue.receive_messages(MessageAttributeNames=['id']):
             id_text = ''
             print(message)
             if message.message_attributes is not None:
                id_text = message.message_attributes.get('id').get('StringValue')
                registro_en_db = signal.query.filter(str(signal.id) == id_text).first()
                if( registro_en_db is not None):
                    print("if",id_text)
                    print("el registro existe en DB")
                    message.delete()
              #      delete_queue_message
                else :
                    print("else",id_text)
                    print("NO  existe en DB")
                    print("message.body" , message.body)
                    postJson(message.body)
                    message.delete()
             

        
   