import os
import time
from slackclient import SlackClient
import pandas

plans = []
t1 = []
temp = []

df = pandas.read_csv('out_data.csv')

for j in range(len(df)):
    for i in df.loc[j]:
        t1.append(str(i))
    temp.append(t1)
    t1=[]

for i in temp:
    plans.append(' '.join(i))

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(temp):
    response = "Give me the corrent input such as @tikonabot broadband or br!"
    print plans

    if('broadband' in temp[0]):
        response = "Wait a min...your plans are coming shortly!!!"

        slack_client.api_call('chat.postMessage',channel=temp[1],text=' \n'.join(plans),as_user=True)
    else:
        slack_client.api_call('chat.postMessage',channel=temp[1],text=response,as_user=True)


def parse_output(slack_rtm_read):
    outList = slack_rtm_read

    if outList and outList>0:
        for output in outList:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(),output['channel']


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    temp =[]
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            temp= parse_output(slack_client.rtm_read())
            if(temp):
                handle_command(temp)

    else:
        print("Connection failed. Invalid Slack token or bot ID?")