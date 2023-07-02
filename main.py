from codecs import getdecoder
from pkgutil import get_data
from highrise import BaseBot, SessionMetadata, User
from highrise.models import Item, Position, AnchorPosition, User
from os.path import exists
from src.handlers.handleCommands import CommandHandler, CommandHandler_DMs, CommandHandler_Whispers
from json import load, dump
from datetime import datetime
import requests


class Bot(BaseBot):
    lobby = {}
    HeistBot_ID = "6497a3527c608ca6fd6c40ab"
    PatrolBot_ID = "6498d86a8ac042a17ce08a4b"
    SpillyMilly_ID= "62fb30c5132e425314f6758f"
    DM_SpillyMilly = "1_on_1:62fb30c5132e425314f6758f:6497a3527c608ca6fd6c40ab"
    outer_vault_pos = Position(10.0, 5.0, 28.5)
    jail_pos = Position(13.5, 11.5, 1.5)
    user_info ={}
    anchorLocations = {'6498976c0000000000000408': ('jail', [15.5, 11.5, 1.5]),
                       '6496ab310000000000000ade': ('bank', [8.5, 11.5, 22.5]),
                       '6496aa290000000000000ab3': ('airballoon',[1.5, 11.0, 2.5]),
                       '6498a34f0000000000000699': ('wandering',[3.5, 10.5, 27.5]),
                       '6498a356000000000000069b': ('wandering',[7.5, 11.0, 18.5]),
                       '649906030000000000000125': ('wandering', [4.5, 11.0, 22.5])}
    base_URL = "https://webapi.highrise.game/"
    HouseofIta_ID = '630f3c84556e38583e114f2b'
    win_delay ={}

    """""
    Notes:
    Game Stages 
        0 - Roof & Outside of Vault
        1 - In bank
        2 - Has stood in fron of Vault, code breaking, Game Lost, jail 
        3 - Has solved code, in Vault
        4 - in Sewers
        5 - Game Won, Air balloon


    """""

    def  __init__(self):
        self.command_handler = CommandHandler(self)
        self.command_handler_whispers = CommandHandler_Whispers(self)
        self.command_handler_dms = CommandHandler_DMs(self)
        super().__init__()

    async def on_start(self, session_metadata: SessionMetadata) -> None:

        print("[START  ]")
        # print(f"{self.get_data()}")
        await self.highrise.teleport(self.HeistBot_ID, Position (11.5, 18.5 ,24.5))
        # await self.highrise.walk_to(AnchorPosition('6497a64500000000000009bc', 0))
        await self.highrise.chat("[Reconnecting...] One moment! I'm preparing the heist again. I might have lost your progress, sorry! \nSay /replay to start over. ") 

        self.user_info = await self.load_data()
        await self.sync_in_room() 
        # print(await self.in_room_ids_dict())

    async def on_user_join(self, user: User) -> None:
        """On a user joining the room."""
        print(f"[JOIN   ] {user.username}")
        if user.id == self.PatrolBot_ID:
            pass
        on_roof = await self.check_if_roof(user.id)
        if on_roof:
            if user.id not in self.user_info:
                await self.whisper(user.id,f"{user.username}, glad you could make it to the Bank Heist, we needed you!")
                await self.whisper(user.id,"To access the vault, you have to crawl into this vent to get inside the bank! \n(Find the teleporter)")
                await self.whisper(user.id,"Say /help or /plan if you ever get confused.")
                await self.reset_user_stage(user)  
                await self.add_default_user(user)
            else:
                # add = '/users/'+user.id
                # user_web_info = requests.get(url = self.base_URL+add, params = {})
                # if user_web_info.json()["user"]["crew"]:    
                #         if user_web_info.json()["user"]["crew"]["id"] == '630f3c84556e38583e114f2b':
                #             await self.whisper(user.id,f"Oooh, {user.username}, you're from House of Ita! Milly loves you!")
                await self.reset_user_stage(user)
                await self.whisper(user.id,"To access the vault, you have to crawl into this vent to get inside the bank!\n(Find the teleporter)\nSay /help if you are confused")
                



    async def on_user_leave(self, user: User) -> None:
        """On a user leaving the room."""
        print(f"[LEAVE  ] {user.username}")

    async def on_channel(self, sender_id: str, message: str, tags: set[str]) -> None:
        """On a hidden channel message."""
        pass
           

    async def on_chat(self, user: User, message: str) -> None:
        print(f"[CHAT   ] {user.username}: {message}")
        if 'how' in message.split() or 'How' in message.split():
            message = "/help"
            await self.command_handler.handlecommand(user, message)
            return
        if message.lstrip().startswith('/enter'):
            await self.highrise.chat("Shh.. you have to whisper to crack the code!! Put @HeistBot at the start of your message to whisper. Example:\n@HeistBot 1234")
        if message.lstrip().startswith('/'):
            parts = message.split()
            if parts[0].isdigit() and len(parts[0]) == 4:
                await self.highrise.chat("Shh.. you have to whisper to crack the code!! Put @HeistBot at the start of your message to whisper. Example:\n@HeistBot 1234")
            await self.command_handler.handlecommand(user, message)
        partial_commands = ["help","info","Help","Info"]
        if message in partial_commands:
            message = "/" + message
            await self.command_handler.handlecommand(user, message)
        if len(message.split()) == 1:
            if message.isdigit() and len(message) == 4:
                await self.highrise.chat("Shh.. you have to whisper to crack the code!! Put @HeistBot at the start of your message to whisper. Example:\n@HeistBot 1234")

        
    async def on_whisper(self, user: User, message: str) -> None:
        """On a whisper."""
        print(f"[WHISPER] {message}")
        if message.lstrip().startswith('/'):
            parts = message.split()
            first_part = parts[0]
            # print(first_part[1:])
            if first_part[1:].isdigit() and len(first_part[1:]) == 4:
                message = f"/enter {first_part[1:]}"
            await self.command_handler_whispers.handlecommand(user, message)
        elif len(message.split()) == 1:
            if message.isdigit() and len(message) == 4:
                    message = f"/enter {message}"
            await self.command_handler_whispers.handlecommand(user, message)
        
        # print((await self.check_position(user.id)))

    async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool):
        results = (await self.highrise.get_messages(conversation_id)).messages
        message = results[0].content
        # print(message)
        if message.lstrip().startswith('/'):
            # print(conversation_id)
            # user_id = conversation_id.split('1_on_1:')[1].split(':')[0]
            await self.command_handler_dms.handlecommand(user_id, conversation_id, message)





    async def on_emote(self, user: User, emote_id: str, receiver: User | None) -> None:
        """On a received emote."""
        if user.id == self.PatrolBot_ID:
            pass
        else:
            print(f"[EMOTE  ] {emote_id} {receiver}")


    async def on_user_move(self, user: User, destination: Position | AnchorPosition) -> None:
        if user.id == self.PatrolBot_ID:
            pass
        else:
            # self.log_location(user, destination)
            # print(await self.check_position(user.id))
            position = str(destination).split()
            if position[0].startswith('AnchorPosition') and self.user_info[user.id]["game_stage"]==4:
                anchor_id = position[0].lstrip("AnchorPosition(entity_id=")[1:-2]
                if anchor_id == '6496aa290000000000000ab3':
                    await self.register_win(user)

            if user.id not in self.user_info:
                await self.add_default_user(user)
    
            stage = self.user_info[user.id]["game_stage"]
            match stage:
                case 0: # roof 
                    await self.check_in_bank(user.id)
                    await self.check_if_out_vault(user, destination)
                case 1: # in bank
                    await self.check_if_out_vault(user, destination)
                case 2: # code breaking stage
                    await self.check_in_bank(user.id)
                    await self.check_if_out_vault(user, destination)
                case 3: # after solving code
                    if self.user_info[user.id]["location"] != 'sewers': # got out of vault
                        await self.check_if_entered_sewers(user, destination)
                case 4: #check where in vault
                    if self.user_info[user.id]["location"] == 'sewers': # in sewers mid and end
                        await self.check_if_sewers_II(user, destination)
                    if self.user_info[user.id]["location"] == 'sewers-II': # in sewers mid and end
                        await self.check_if_escaped_sewers(user, destination)
                
               



    def get_data(self):
        with open("./data.json", "r") as file:
            data = load(file)
        return data

    async def add_default_user(self, user: User):
        default_info = {
                    "user_id": user.id,
                    "username": user.username,
                    "game_stage": 0,
                    "location": 'roof',
                    "wins": 0,
                    "losses":0,
                    "code_attempts": 0,
                    "current_code": 'XXXX',
                    "answer_code":'XXXX',
                    "eliminated_digits": [],
                    }
        self.user_info[user.id] = default_info

    async def check_if_out_vault(self,user,pos):
        position = str(pos).split()
        if position[1][:-1].startswith('anchor_ix='):
            return 0
        y = float(position[1].lstrip("y=")[:-1])
        x = float(position[0].lstrip("Position(x=")[:-1])
        if y == 5.0 and x < 12.5:
            # print("Outside of vault.")
            # print(self.user_info)
            stage = self.user_info[user.id]["game_stage"]
            if stage == 1 or stage == 0:
                await self.whisper(user.id,"You made it to the vault! Now to break the code...")
                await self.whisper(user.id,"I can disable the security system for 10 code attempts, any longer and the police will catch you!")
                await self.whisper(user.id,"Think of any 4 digit code [ex: 1234] then \nwhisper @HeistBot 1234")
                self.user_info[user.id]["game_stage"]= 2 #update to code-stage 
                self.user_info[user.id]["location"] = 'out-vault' #update to code-stage 
                return 1

            if stage == 2 and self.user_info[user.id]["location"] != 'in-vault':
                await self.whisper(user.id,"Let's get cracking! Think of a 4 digit code [ex: 1234] and \nwhisper it to @HeistBot")
                self.user_info[user.id]["location"] = 'out-vault' #update location

                return 1
            
        else:
            return 0
        
    async def check_position(self, user_id):
       in_room = (await self.highrise.get_room_users()).content
       user_pos_dict = {user[0].id: user[1] for user in in_room}
       if user_id not in user_pos_dict.keys():
           return ['0.0','0.0','0.0'] #uhhh bruh idk what to do here
       pos = str(user_pos_dict[user_id])
       
       pos = pos.split()

       if pos[0].startswith('AnchorPosition'):
           anchor_id = pos[0].lstrip("AnchorPosition(entity_id=")[1:-2]
           location_name = self.anchorLocations[anchor_id][0]
           self.user_info[user_id]["location"] = location_name
           position = self.anchorLocations[anchor_id][1]
           await self.save_data()
           return position
       x = pos[0].lstrip("Position(x=")[:-1]
       y = pos[1].lstrip("Position(y=")[:-1]
       z = pos[2].lstrip("Position(z=")[:-1]
       user_position_array = [x, y, z]

       return user_position_array
    
    async def check_if_roof(self, user_id):
        position = await self.check_position(user_id)
        if position[1] == '18.0':
            return 1
        else:
            return 0
        
    async def check_in_bank(self, user_id):
        position = await self.check_position(user_id)
        # print(f"checking in bank, current position:{position}")
        if position[1] == '11.5' and float(position[2]) >= 22.0:
            stage = self.user_info[user_id]["game_stage"]
            if stage == 0:
                await self.whisper(user_id,"Nice! You made in into to the bank. Now walk down to the vault! \n(Tap in front of vault door)")
                self.user_info[user_id]["location"] = 'bank'
                self.user_info[user_id]["game_stage"] = 1 #update stage to bank stage
                return 1
            self.user_info[user_id]["location"] = 'bank'
            return 1
        else:
            return 0
    
    async def check_if_escaped_sewers(self,user,pos):
        # print("checking if escaped sewers...")
        position = str(pos).split()
        if position[1][:-1].startswith('anchor_ix='):
            return 0
        y = float(position[1].lstrip("y=")[:-1])
        x = float(position[0].lstrip("Position(x=")[:-1])
        if y == 11.0 and x <6.0:
            await self.register_win(user)

            return 1
            
        else:
            return 0
        
    async def register_win(self, user):
        now = datetime.now()                
        if user.id in self.win_delay:
            win_time = self.win_delay[user.id]
            time_since_caught = now - win_time
            # print("Time since caught:", time_since_caught)
            if time_since_caught.total_seconds() < 3:
                return
            # result = remaining_time.strftime("%H:%M")
        
        self.win_delay[user.id] = now
        print("Escaped sewers!")
        self.user_info[user.id]["wins"] += 1
        
        wins = self.user_info[user.id]["wins"]
        await self.highrise.chat(f"\U0001F4B0 \U0001F4B0 {user.username} has escaped and suceeded on their heist!\U0001F4B0 \U0001F4B0")
        await self.whisper(user.id,f"Congrats!! You made it out! \nYou have suceeded on {wins} Bank Heist(s)")
        if self.user_info[user.id]["wins"] == 1:
            await self.highrise.send_message(self.DM_SpillyMilly, f"NEW WINNER: {user.username}")
            await self.whisper(user.id,f"Post a pic in the air balloon with #BankHeist! @SpillyMilly might give you a prize!")

        self.user_info[user.id]["game_stage"]= 5 #update to win stage
        self.user_info[user.id]["location"] = 'airballoon' #update to code-stage 
        await self.whisper(user.id,f"Say /replay to play the game again!")

        await self.save_data()


        
    
    async def check_if_entered_sewers(self,user,pos):
        position = str(pos).split()
        # print(pos)
        if position[1][:-1].startswith('anchor_ix='):
            return 0
        y = float(position[1].lstrip("y=")[:-1])
        if y < 2.0 and self.user_info[user.id]["location"] != 'sewers':
            print("Entered sewers!")
            stage = self.user_info[user.id]["game_stage"]
            if stage != 3:
                await self.whisper(user.id,"I am so confused...")
                self.user_info[user.id]["location"] = 'sewers'
                self.user_info[user.id]["game_stage"] = 4
                return 1

            else:
                self.user_info[user.id]["location"] = 'sewers'
                await self.whisper(user.id,f"Get through the sewers to bring the gold to our escape air balloon!")
                self.user_info[user.id]["game_stage"] = 4
                await self.save_data()
                return 1
            
        else:
            return 0
        
    async def check_if_sewers_II(self,user,pos):
        position = str(pos).split()
        # print(pos)
        if position[1][:-1].startswith('anchor_ix='):
            return 0
        y = float(position[1].lstrip("y=")[:-1])
        x = float(position[0][11:-1])
        z = float(position[2].lstrip("z=")[:-1])
        if y < 2.0 and x < 4.0 and z < 27.5:
            print("Entered sewers II!")
            stage = self.user_info[user.id]["game_stage"]
            if stage != 4:
                await self.whisper(user.id,"I am so confused...")
                self.user_info[user.id]["location"] = 'sewers-II'
                self.user_info[user.id]["game_stage"] = 4
                return 1

            else:
                self.user_info[user.id]["location"] = 'sewers-II'
                await self.whisper(user.id,f"Wait! Do you see @PatrolBot? Don't get caught, he'll send you straight to jail!") 
                await self.whisper(user.id,"(Avoid being seen by @PatrolBot)")
                self.user_info[user.id]["game_stage"] = 4
                await self.save_data()
                return 1
            
        else:
            return 0
        
    async def reset_user_stage(self,user:User):
        await self.load_data()
        if user.id not in self.user_info:
            await self.add_default_user(user)
        else:
            self.user_info[user.id]["game_stage"]= 0
            self.user_info[user.id]["location"] = 'roof'
            await self.save_data()

    async def sync_users(self):
        in_room = (await self.highrise.get_room_users()).content
        user_ids = {user[0].id: user[0].username for user in in_room}
        with open("./data.json", "r+") as file:
            data = load(file)
            file.seek(0)
            for id in user_ids:
                if not id in self.get_data().keys() and id != self.HeistBot_ID and id != self.PatrolBot_ID:
                    
                        if id in data:
                            print(f"User: {user_ids[id]} exists.")
                        else:
                            username = user_ids[id]

                            data[id] = {
                                "username": username,
                                "user_id": id
                            }
                            print(f"Added new user {user_ids[id]}.")
            
            dump(data, file)
            file.truncate()

    async def save_data(self):
        with open("./data.json", "r+") as file:
            data = load(file)
            file.seek(0)
            for session_user in self.user_info:
                data[session_user] = self.user_info[session_user]      
            dump(data, file)
            file.truncate()

    async def load_data(self):
        with open("./data.json", "r+") as file:
            data = load(file)
            file.seek(0)
            for session_user in self.user_info:
                data[session_user] = self.user_info[session_user]      
            dump(data, file)
            file.truncate()
        return data

    async def check_save(self, user: User):
        with open("./data.json", "r+") as file:
            data = load(file)
            file.seek(0)
            if user.id in data:
                self.user_info[user.id] = data[user.id]
                dump(data, file)
                file.truncate()
                return 1
            else:
                dump(data, file)
                file.truncate()
                return 0
    
    async def sync_in_room(self):
        in_room = (await self.highrise.get_room_users()).content
        user_ids = {user[0].id: user[0].username for user in in_room}
        positions = {user_id: await self.check_position(user_id) for user_id in user_ids}


        for user in positions:
            user_x = float(positions[user][0])
            user_y = float(positions[user][1])
            user_z = float(positions[user][2])
            if user not in self.user_info:
                default_info = {
                    "user_id": user,
                    "username": user_ids[user],
                    "game_stage": 0,
                    "location": 'roof',
                    "wins": 0,
                    "losses":0,
                    "code_attempts": 0,
                    "current_code": 'XXXX',
                    "answer_code":'XXXX',
                    "eliminated_digits": [],
                    }
                self.user_info[user] = default_info
            await self.get_location_from_pos(user, [user_x, user_y, user_z])
            
            # print(f"{user_ids[user]} updated to location: {self.user_info[user]['location']}")
            await self.save_data()
    
    async def in_room_ids_dict(self):
        in_room = (await self.highrise.get_room_users()).content
        user_ids = {user[0].id: user[0].username for user in in_room}
        return user_ids
    
    async def in_room_names_dict(self):
        in_room = (await self.highrise.get_room_users()).content
        user_ids = {user[0].username: user[0].id for user in in_room}
        return user_ids
    
    
    async def whisper(self, user_id, message) -> None:
        try:
            await self.highrise.send_whisper(user_id, message)
        except Exception as e:
            print(f"Caught Whisper Error: {e}")
        
    def log_location(self,user,destination):
        try:
            if isinstance(destination, AnchorPosition):
                # Destination is an anchor
                entity_id = destination.entity_id
                anchor_ix = destination.anchor_ix
                print(
                    f"{user.username} moved to (entity_id: {entity_id} anchor_ix: {anchor_ix})")
            elif isinstance(destination, Position):
                # Destination is a position
                x = destination.x
                y = destination.y
                z = destination.z
                facing = destination.facing
                print(
                    f"{user.username} moved to ({x}x, {y}y, {z}z, {facing})")
            else:
                # Invalid destination type
                print("Invalid destination type")
        except Exception as e:
            # Handle any exceptions that occur during the logging process
            print(f"Error logging user move: {e}")

    async def get_location_from_pos(self, user_id, position):
        
            in_room = (await self.highrise.get_room_users()).content
            user_ids = {user[0].id: user[0].username for user in in_room}
 
            user_x = float(position[0])
            user_y = float(position[1])
            user_z = float(position[2])
            if user_id not in self.user_info:
                default_info = {
                    "user_id": user_id,
                    "username": user_ids[user_id],
                    "game_stage": 0,
                    "location": 'roof',
                    "wins": 0,
                    "losses":0,
                    "code_attempts": 0,
                    "current_code": 'XXXX',
                    "answer_code":'XXXX',
                    "eliminated_digits": [],
                    }
                self.user_info[user_id] = default_info
            # print(f"User {user_ids[user]} in room already")
            if user_x > 10.0 and user_y >= 17.5 and user_z > 20:
                self.user_info[user_id]["location"] = 'roof'
                self.user_info[user_id]["game_stage"] = 0
                return 'roof'
            elif user_x > 8.0 and user_y < 14.0 and user_y >= 11.5 and user_z > 22.0:
                self.user_info[user_id]["location"] = 'bank'
                self.user_info[user_id]["game_stage"] = 1
                return 'bank'
            elif user_y == 5.0 and user_x < 12.5:
                self.user_info[user_id]["location"] = 'out-vault'
                self.user_info[user_id]["game_stage"] = 2
                return 'out-vault'
            elif user_y == 5.0 and user_x > 12.5:
                self.user_info[user_id]["location"] = 'in-vault'
                self.user_info[user_id]["game_stage"] = 3
                return 'in-vault'
            elif user_y <= 2.0:
                self.user_info[user_id]["location"] = 'sewers'
                self.user_info[user_id]["game_stage"] = 4
                return 'sewers'
            elif user_y < 2.0 and user_x < 4.0 and user_z < 27.5:
                self.user_info[user_id]["location"] = 'sewers-II'
                self.user_info[user_id]["game_stage"] = 4
                return 'sewers-II'
            elif user_y == 11.0 and user_x <6.0:
                self.user_info[user_id]["location"] = 'airballoon'
                self.user_info[user_id]["game_stage"] = 5
                return 'airballoon'
            elif user_y == 11.5 and user_x >= 13.5 and user_z < 6.0:
                self.user_info[user_id]["location"] = 'jail'
                self.user_info[user_id]["game_stage"] = 5
                return 'jail'
            elif user_y > 15.5 and user_x >= 12.5 and user_z < 15.0:
                self.user_info[user_id]["location"] = 'jail_roof'
                self.user_info[user_id]["game_stage"] = 5
                return 'jail_roof'
            else:
                self.user_info[user_id]["location"] = 'wandering'
                self.user_info[user_id]["game_stage"] = 5
                return 'wandering'
            
            # print(f"{user_ids[user]} updated to location: {self.user_info[user]['location']}")
            await self.save_data()