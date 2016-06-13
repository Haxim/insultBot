import time
import random
import requests
import json
from slackclient import SlackClient

token = "xoxp-28192348123947234198234" # found at https://api.slack.com/web#authentication
botName = "botName"
botChance = 5 #5 = 0.5% chance of text triggering an insult 10 = 1%, etc
botChannel = "#general"

def botSpeak ( botText ):
    sc.api_call("chat.postMessage", channel=botChannel, text=botText, as_user="true", username=botName, link_names=1)

sc = SlackClient(token)
if sc.rtm_connect():
    while True:
        new_evts = sc.rtm_read()
        for evt in new_evts:
            print(evt)
            foaasChance = random.randint(1,1000)
            if "type" in evt:
                if evt["type"] == "message" and "text" and "user" in evt and "bot_id" not in evt:
                    message=evt["text"]
                    user = "<@" + evt["user"] + ">"
                    if foaasChance <= botChance:
                        url = 'http://www.foaas.com/operations'
                        headers = {'Accept': 'application/json'}
                        r = requests.get(url, headers=headers)
                        foaas = json.loads(r.text)
                        badurl = 1
                        while (badurl == 1):
                            action = random.choice(foaas)
                            url = action['url']
                            url = url.replace(':from', botName)
                            url = url.replace(':name', user)
                            url = 'http://www.foaas.com' + url
                            if '/:' not in url:
                                badurl = 0
                        r = requests.get(url, headers=headers)
                        foaasMessage = json.loads(r.text)
                        botSpeak ( botText = foaasMessage['message'] )
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"
