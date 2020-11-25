# app.py

import boto3

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

if __name__ == '__main__':
     messages_table = create_messages_table()
     print("Table status:", messages_table.table_status)