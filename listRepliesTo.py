from pprint import pprint
import boto3
from botocore.exceptions import ClientError


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


if __name__ == '__main__':
    # Must pass the msgID along with the recipient since the msgID is a key. If not, we get the error "The number of conditions on teh keys is invalid"
    message = listRepliesTo("Adam", 4603)
    if message:
        print("List replies succeeded:")
        pprint(message, sort_dicts=False)