#!/usr/bin/env python

import sys

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class Slack:
    ARGS, SERV, HEAD, ERRS, ENVS = 4, 1, 2, 3, 4

def send_to_slack(slack_token, channel, server, headline, error_text):

    # Set up the WebClient using the Bot User OAuth Access Token
    # client = WebClient(token=os.environ[swatchdog_token])
    client = WebClient(token=slack_token)

    # The JSON message to send to the channel
    message = 'swatchdog alert - host: ' + server + '. ' + headline + ' : ' + error_text

    try:
        # Send the message to the channel
        response = client.chat_postMessage(channel=channel, text=message)

        # Print the response from the API
        # print(response)

    except SlackApiError as e:
        # Print any error messages returned by the API
        print(f"Error sending message: {e}.")
        print(f"Message would have been: {message}")

if __name__ == '__main__':
    if len(sys.argv) <= Slack.ARGS:
        print(f"Must be {Slack.ARGS} arguments: {sys.argv}")
        exit(-1)
    
    with open(sys.argv[Slack.ENVS]) as envs:
        # Read environment
        env = dict(v.strip().split('=') for v in envs.readlines())

        send_to_slack(
            env['SLACK_TOKEN'], env['SLACK_CHANNEL'], 
            sys.argv[Slack.SERV], sys.argv[Slack.HEAD], sys.argv[Slack.ERRS])