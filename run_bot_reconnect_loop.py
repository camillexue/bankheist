import yaml
import os
from time import sleep
import sys

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

room_id = config.get("room_id")
api_token = config.get("api_token")
file_name = config.get("file_name")
bot2 = '5cdaeeac713f26c51fa6d835cf0d0f6f1a8753cef247d53d45bc453adbc185dd'
path = config.get("file_name2")
fails = 0


class runner:
    def __init__(self):
       self.fails = 0

   
    def run_forever(self):
        try:
            # Create infinite loop to simulate whatever is running
            # in your program
            while True:
                print("Hello!")
                sleep(10)
                if not room_id or not api_token:
                    print("Please set the room_id and api_token in config.yml.")
                else:
                    os.system(f"highrise {file_name}:Bot {room_id} {api_token} --extra_bot {path}:Bot {room_id} {bot2}")

                # Simulate an exception which would crash your program
                # if you don't handle it!
                # raise Exception("Error simulated!")
            
        except ConnectionResetError:
            self.handle_exception()

        except Exception:
            print("Something crashed your program. Let's restart it")
            # run_forever() # Careful.. recursive behavior
            # Recommended to do this instead          
            self.handle_exception()

    def handle_exception(self):
        self.fails += 1
        sleep(10)
        self.run_forever()


start = runner()
start.run_forever()