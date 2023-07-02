import requests
import json


base_URL = "https://webapi.highrise.game/"
HouseofIta_ID = '630f3c84556e38583e114f2b'
user_id='62fb30c5132e425314f6758f'
# defining a params dict for the parameters to be sent to the API
PARAMS = {}
add = '/users/'+'6497a3527c608ca6fd6c40ab'
user_web_info = requests.get(url = base_URL+add, params = PARAMS)
if user_web_info.json()["user"]["crew"]:    
    print(user_web_info.json()["user"]["crew"]["id"])
else:
    print("no crew")