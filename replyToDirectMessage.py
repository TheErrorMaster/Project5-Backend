from pprint import pprint
import boto3, random

def replyToDirectMessage(msgID, recipient, sender, reply, quick_reply=None, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

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


if __name__ == '__main__':
    # replyToDirectMessage( <original msgID>, 
    # this is the recipient <SELECT sender WHERE msgID == original msgID>, 
    # this is the sender    <SELECT recipient WHERE msgID == original msgID>, 
    #                       <reply>, 
    #                       <quick_reply> )
    message_resp = replyToDirectMessage(1805, "Adam", "Mike", "This is a test reply.",3)
    print("Put reply succeeded:")
    pprint(message_resp, sort_dicts=False)
