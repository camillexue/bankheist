from codecs import getdecoder
from pkgutil import get_data
from highrise import BaseBot, SessionMetadata, User
from highrise.models import Item, Position, AnchorPosition
from os.path import exists
from src.handlers.handleCommands import CommandHandler, CommandHandler_DMs, CommandHandler_Whispers
from json import load, dump
import asyncio
from asyncio import run as arun
from datetime import datetime



class Bot(BaseBot):
    lobby = {}
    PatrolBot_ID = "6498d86a8ac042a17ce08a4b"
    SpillyMilly_ID= "62fb30c5132e425314f6758f"
    outer_vault_pos = Position(10.0, 5.0, 28.5)
    jail_pos = Position(13.5, 11.5, 1.5)
    temp_jail_pos = Position(3.5,  0.5, 25.5)
    user_info ={}
    walk_path = True
    sewer_player_positions = {}
    path = 'AB'
    caught_delay = {}
    current_pos = 7.5
    direction = 1
    anchorLocations = {'6498976c0000000000000408': ('jail', [15.5, 11.5, 1.5]),
                       '6496ab310000000000000ade': ('bank', [8.5, 11.5, 22.5]),
                       '6496aa290000000000000ab3': ('airballoon',[1.5, 11.0, 2.5]),
                       '6498a34f0000000000000699': ('wandering',[3.5, 10.5, 27.5]),
                       '6498a356000000000000069b': ('wandering',[7.5, 11.0, 18.5]),
                       '649906030000000000000125': ('wandering', [4.5, 11.0, 22.5])}

    def  __init__(self):
        self.command_handler = CommandHandler(self)
        self.command_handler_whispers = CommandHandler_Whispers(self)
        super().__init__()
        

    async def on_start(self, session_metadata: SessionMetadata) -> None:

        print("[START  ]")
        # print(f"{self.get_data()}")
        await self.reload_user_info()
        await self.sewer_position_updater()
        time_delay = 5
        await self.highrise.teleport(self.PatrolBot_ID, Position (0.5, 0.5,6.5))
        # loop = asyncio.get_event_loop()
        # loop.create_task(self.forever_walk())
        # loop.create_task(self.forever_check())
        self.highrise.tg.create_task(self.forever_walk())
        self.highrise.tg.create_task(self.forever_check())


    async def on_user_move(self, user: User, destination: Position | AnchorPosition) -> None:
        if user.id == self.PatrolBot_ID:
            pass
        else:
            position = str(destination).split()
            if position[1][:-1].startswith('anchor_ix='):
                return 0
            x = float(position[0].lstrip("Position(x=")[:-1])
            y = float(position[1].lstrip("y=")[:-1])
            z = float(position[2].lstrip("z=")[:-1])
            if y > 3.0 or x > 3.0:
                pass
            else:
                await self.check_caught_move(user.id, [x, y, z])

    async def forever_walk(self):
        while True:
            await self.walk_loop()

    async def forever_check(self):
        while True:
            await self.sewer_position_updater()
            await self.check_all_sewers_caught()

    async def walk_loop(self):
        time_delay = 2
        start = 6.5
        end = 18.5
        step = 2.0
        

        await self.reload_user_info()
        if self.direction and self.current_pos == end:
            dest = self.current_pos - step
            self.direction = 0
        
        elif self.direction and self.current_pos <= end:
            dest = self.current_pos + step

        elif not self.direction and self.current_pos == start:
            
            dest = self.current_pos + step
            self.direction = 1

        elif not self.direction and self.current_pos >= start:
            dest = self.current_pos - step

        else:
            dest = start

        if self.direction:
            facing = "FrontRight"
        else:
            facing = 'BackLeft'
    
        self.current_pos = dest
        
        await asyncio.sleep(time_delay)
        await self.highrise.walk_to(Position (0.5, 0.5, dest,facing)) #to A        
    
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
       else:
            x = pos[0].lstrip("Position(x=")[:-1]
            y = pos[1].lstrip("Position(y=")[:-1]
            z = pos[2].lstrip("Position(z=")[:-1]
            user_position_array = [x, y, z]

            return user_position_array
    


    async def walk_to_pos(self, pos):
        time_delay = 5
        await self.highrise.walk_to(pos)
        await asyncio.sleep(time_delay)

    async def sewer_position_updater(self):            
        in_room = (await self.highrise.get_room_users()).content
        user_pos_dict = {user[0].id: user[1] for user in in_room}
        sewer_locatons = {}
        for user in user_pos_dict:
            if user == self.PatrolBot_ID:
                break
            pos = str(user_pos_dict[user])
            pos = pos.split()
            if pos[0].startswith('AnchorPosition'):
                anchor_id = pos[0].lstrip("AnchorPosition(entity_id=")[1:-2]
                location_name = self.anchorLocations[anchor_id][0]
                self.user_info[user]["location"] = location_name
                position = self.anchorLocations[anchor_id][1]
                sewer_locatons[user] = position
                await self.save_data()
            else:
                x = pos[0].lstrip("Position(x=")[:-1]
                y = pos[1].lstrip("Position(y=")[:-1]
                z = pos[2].lstrip("Position(z=")[:-1]
                user_position_array = [x, y, z]
                if float(y) < 3.0:
                    sewer_locatons[user] = user_position_array
        self.sewer_player_positions = sewer_locatons
    

    async def check_all_sewers_caught(self):
        sewer_players = self.sewer_player_positions
        for player in sewer_players:
            if player == self.PatrolBot_ID:
                break
            await self.check_caught(player, sewer_players[player])

    async def check_caught(self, user_id, position):
        player = user_id
        if user_id == self.PatrolBot_ID:
            return
        else:
            player_x = float(position[0])
            player_y = float(position[1])
            player_z = float(position[2])
           
            if player_x > 3.0 or player_y > 3.0:
                return
            
            if self.direction:
                min = self.current_pos + 1.5
                max = self.current_pos + 3.5
            
            else:
                min = self.current_pos - 3.5
                max = self.current_pos - 1.5
                        
            if player_z > min and player_z < max and player_z > 7.0:
                #player is caught
                now = datetime.now()
                
                if player in self.caught_delay:
                    caught_time = self.caught_delay[player]
                    time_since_caught = now - caught_time
                    # print("Time since caught:", time_since_caught)
                    if time_since_caught.total_seconds() < 5:
                        return
                    # result = remaining_time.strftime("%H:%M")
                await self.caught(player)
        return 
    
    async def check_caught_move(self, user_id, position):
        player = user_id
        if user_id == self.PatrolBot_ID:
            return
        else:
            player_x = float(position[0])
            player_y = float(position[1])
            player_z = float(position[2])
           
            if player_x > 3.0 or player_y > 3.0:
                return
            
            if self.direction:
                min = self.current_pos - 2.5
                max = self.current_pos + 3.5
            
            else:
                min = self.current_pos - 3.5
                max = self.current_pos + 2.5
                        
            if player_z > min and player_z < max and player_z > 7.0:
                #player is caught
                now = datetime.now()
                
                if player in self.caught_delay:
                    caught_time = self.caught_delay[player]
                    time_since_caught = now - caught_time
                    # print("Time since caught:", time_since_caught)
                    if time_since_caught.total_seconds() < 5:
                        return
                    # result = remaining_time.strftime("%H:%M")
                await self.caught(player)
        return 
    
    async def caught(self,player):
        now = datetime.now()
        try:
            await self.highrise.teleport(player, self.jail_pos) 
            self.user_info[player]["losses"] += 1
            self.user_info[player]["location"] = 'jail'
            ids_user = await self.in_room_ids_dict()
            username = ids_user[player]
            await self.whisper(player,f"{username}! YOU GOT CAUGHT! You're in jail. Try again!")
            await self.highrise.chat(f"\U0001F6A8 {username} WAS CAUGHT! \U0001F6A8\nThey got sent to jail.")
            # print(f"Player {username} was caught at {player_z} when bot was at {self.current_pos} and facing {self.direction}.")
            self.caught_delay[player] = now
            await self.update_user_jailed(player)
            
        except Exception as e:
            print(f"Caught tele Error: {e}")

   

    async def update_user_jailed(self, playerid):
        with open("./data.json", "r+") as file:
            data = load(file)
            data[playerid]["game_stage"] = 5
            data[playerid]["losses"] += 1
            data[playerid]["location"] = 'jail'
            losses = data[playerid]["losses"]
            await self.whisper(playerid, f"You have been caught {losses} time(s). Use /replay to play again!")
            file.seek(0)
            dump(data, file)
            file.truncate()
       

    async def sewer_positions(self):
    
       in_room = (await self.highrise.get_room_users()).content
       user_pos_dict = {user[0].id: user[1] for user in in_room}
       sewer_locatons = {}
       for user in user_pos_dict:
            pos = str(user_pos_dict[user])
            pos = pos.split()
            if len(pos) == 3:
                x = pos[0].lstrip("Position(x=")[:-1]
                y = pos[1].lstrip("Position(y=")[:-1]
                z = pos[2].lstrip("Position(z=")[:-1]
                if y < 3.0 and x < 3.0:
                    user_position_array = [x, y, z]
                    sewer_locatons[user] = user_position_array
       return sewer_locatons
    
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
        return data
    
    async def reload_user_info(self):
        with open("./data.json", "r+") as file:
            data = load(file)
            self.user_info = data
        return data
    
    async def whisper(self, user_id, message) -> None:
        try:
            await self.highrise.send_whisper(user_id, message)
        except Exception as e:
            print(f"Caught Whisper Error: {e}")

    async def in_room_ids_dict(self):
        in_room = (await self.highrise.get_room_users()).content
        user_ids = {user[0].id: user[0].username for user in in_room}
        return user_ids