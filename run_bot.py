import yaml
import os
from time import sleep
import sys

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

room_id = config.get("room_id")
api_token = config.get("api_token")
file_name = config.get("file_name")
api_token2 = config.get("api_token2")
path = config.get("file_name2")


if not room_id or not api_token:
    print("Please set the room_id and api_token in config.yml.")
else:
    os.system(f"highrise {file_name}:Bot {room_id} {api_token} --extra_bot {path}:Bot {room_id} {api_token2}")
