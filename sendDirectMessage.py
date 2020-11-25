from pprint import pprint
import boto3, random

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
    message_resp = sendDirectMessage("Mike", "Adam", "This is a test message.",2)
    print("Put message succeeded:")
    pprint(message_resp, sort_dicts=False)
