# app.py

from pprint import pprint
from flask import Flask, request, jsonify, g
from flask_api import status, exceptions
from botocore.exceptions import ClientError
import click
import boto3, random


app = Flask(__name__, instance_relative_config=True)


def create_messages_table(dynamodb=None):
     if not dynamodb:
          dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
     table = dynamodb.create_table(
          TableName='Messages',
          KeySchema=[
               {
                    'AttributeName': 'msgID',
                    'KeyType': 'HASH'
               },
               {
                    'AttributeName': 'recipient',
                    'KeyType': 'RANGE'
               },
          ],
          AttributeDefinitions=[
               {
                    'AttributeName': 'msgID',
                    'AttributeType': 'N'
               },
               {
                    'AttributeName': 'recipient',
                    'AttributeType': 'S'
               },
          ],
          ProvisionedThroughput={
               'ReadCapacityUnits': 10,
               'WriteCapacityUnits': 10
          }
     )
     return table


@app.route('/reply', methods['POST'])
def replyToDirectMessage():
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    request_data = request.get_json()
    msgID = request_data['msg_id']
    recipient = request_data['recipient']
    sender = request_data['sender']
    reply = request_data['reply']
    quick_reply = request_data.get('quick_reply')
    if request_data.get('quick_reply'):
        # Quick Reply message options
        if quick_reply == 1:
            reply = "Can't talk now."
        elif quick_reply == 2:
            reply = "On my way!"
        elif quick_reply == 3:
            reply = "Hey :)"

    newMsgID = random.randint(0,10000)

    table = dynamodb.Table('Messages')
    response = table.put_item(
       Item={
            'msgID': newMsgID,      # This is a new message, so it will get a new msgID
            'recipient': recipient, # The recipient of the reply is the sender of the original message
            'sender': sender,       # The sender of the reply is the recipient of the original message
            'replyToID': msgID,     # The "replyToID" is the msgID from the original message
            'message': reply,       # The message is the reply
        }
    )
    return response


@app.route('/user/messages', methods=['GET'])
def listDirectMessagesFor(recipient, msgID, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Messages')

    try:
        response = table.get_item(Key={'recipient': recipient, 'msgID': msgID})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


@app.route('/user/replies', methods=['GET'])
def listRepliesTo(recipient, msgID, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Messages')

    try:
        response = table.get_item(Key={'recipient': recipient, 'msgID': msgID})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


@app.route('/message', methods=['POST'])
def sendDirectMessage(recipient, sender, message, quick_reply=None, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    # Quick Reply message options
    if quick_reply == 1:
        message = "Can't talk now."
    elif quick_reply == 2:
        message = "On my way!"
    elif quick_reply == 3:
        message = "Hey :)"

    msgID = random.randint(0,10000)

    table = dynamodb.Table('Messages')
    response = table.put_item(
       Item={
            'msgID': msgID,
            'recipient': recipient,
            'sender': sender,
            'message': message,
        }
    )
    return response


if __name__ == '__main__':
     messages_table = create_messages_table()
     print("Table status:", messages_table.table_status)
