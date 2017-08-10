from __future__ import print_function

import boto3
import json
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

access_code = ''        # BotのAccess Codeを入力
botDisplayName = ''     # Bot名を入力

def sendSparkGET(event):
    url = 'https://api.ciscospark.com/v1/messages/{0}'.format(event.get('data')['id'])
    headers = {
        'Authorization' : 'Bearer ' + access_code,
        'Content-Type' : 'application/json'
    }
    r1 = requests.get(url, headers = headers)
    return json.loads(r1.text)

def sendSparkPOST(event, message_detail):
    url = 'https://api.ciscospark.com/v1/messages/'
    headers = {
        'Authorization' : 'Bearer ' + access_code,
        'Content-Type' : 'application/json'
    }
    payload = {
      "roomId" : event.get('data')['roomId'],
      "text" : 'pong'
    }
    r1 = requests.post(url, headers = headers, data = json.dumps(payload))
    return True

def handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    message_detail = sendSparkGET(event)
    bot_command = message_detail['text']

    bot_commands = {
        botDisplayName + 'ping' : lambda x, y : sendSparkPOST(x, y)
    }

    if bot_command in bot_commands:
        return bot_commands[bot_command](event, message_detail)
    else:
        raise ValueError('Unrecognized operation')
