from flask.json import jsonify
from dotenv import load_dotenv, find_dotenv
import os

import requests
import json
import re

class TwitchHandler:
    url = "https://api.twitch.tv/helix/streams"
    params = {
        "first": 1,
        "after": None
    }

    auth_url= 'https://id.twitch.tv/oauth2/token'
    auth_params = {'client_id': os.getenv('client_id'),
             'client_secret': os.getenv('client_secret'),
             'grant_type': 'client_credentials'
             } 


    def __init__(self):
        load_dotenv(find_dotenv(), verbose=True)

        self.access_token = None
        TwitchHandler.auth_params['client_id'] = os.getenv('client_id')
        TwitchHandler.auth_params['client_secret'] = os.getenv('client_secret'),

    def authenticate(self):
        auth_call = requests.post(url=TwitchHandler.auth_url, params=TwitchHandler.auth_params) 
        self.access_token = auth_call.json()['access_token']

    def fetch_streamer(self, username):
        head = {
            'Client-ID' : TwitchHandler.auth_params['client_id'],
            'Authorization' :  "Bearer " + self.access_token
            }
        
        local_params = {
            'first': 1,
            'after': None,
            'user_login': username
        }

        ret = requests.get(TwitchHandler.url, headers = head, params=local_params).json()
        return ret

        
    def fetch_streamers(self, nb, cursor=None):
        if(nb > 100):
            raise "can only fetch up to 100 streamer at a time"

        head = {
            'Client-ID' : TwitchHandler.auth_params['client_id'],
            'Authorization' :  "Bearer " + self.access_token
            }
    
        TwitchHandler.params['first'] = nb 
        TwitchHandler.params['after'] = cursor   

        ret = requests.get(TwitchHandler.url, headers = head, params=TwitchHandler.params).json()
        TwitchHandler.params['after'] = ret['pagination']['cursor']
        return ret['data']

    def subscribe_to_event(self, id):
        head = {
            'Client-ID' : TwitchHandler.auth_params['client_id'],
            'Authorization' :  "Bearer " + self.access_token,
            'Content-type' : "application/json"
            }
        data = {
            "type": "stream.online",
            "version": "1",
            "condition": {
                "broadcaster_user_id": id
            },
            "transport": {
                "method": "webhook",
                "callback": "https://127.0.0.1:5000/subscriptions/callback",
            }
        }
        ret = requests.post('https://api.twitch.tv/helix/eventsub/subscriptions', headers=head, data=data)
        return ret

    @staticmethod
    def convert_twitch_to_db_format(item):
        rep = {"{width}": "500", "{height}": "500"} # define desired replacements here

        # use these three lines to do the replacement
        rep = dict((re.escape(k), v) for k, v in rep.items()) 
        #Python 3 renamed dict.iteritems to dict.items so use rep.items() for latest versions
        pattern = re.compile("|".join(rep.keys()))
        profil_pic_url = pattern.sub(lambda m: rep[re.escape(m.group(0))], item['thumbnail_url'])
                
        return (item['user_id'], "Twitch", item['user_name'], "www.twitch.tv/" + item['user_name'], profil_pic_url)



if __name__ == "__main__":

    twitch_handler = TwitchHandler()
    acces_token = twitch_handler.authenticate()
    for _ in range(2):
        ret = twitch_handler.fetch_streamers(20, TwitchHandler.params['after'])
        for r in ret:
            #print(TwitchHandler.convert_twitch_to_db_format(r))
            print(r['user_name'])
    #print(twitch_handler.fetch_streamer("SheisouTV"))
