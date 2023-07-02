from highrise import User
import random
from highrise.models import Item, Position, AnchorPosition
from json import load,dump

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'getstats'
        self.description = "User gets their game info"
        self.aliases = ["get", "stats-of"]
        self.permissions = ["inspect"]
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        separated = message.split()
        
        if len(separated) < 2:
            await self.bot.whisper(user.id, "Could not execute stat command, message too short.")
            return

        name = separated[1][1:]
        username_lookup = (await self.bot.in_room_names_dict())
        if name in username_lookup:
            user_id = username_lookup[name]
        else:
            await self.bot.whisper(user.id, "Could not execute stat command, not found in user dict.")
            return

        with open("./data.json", "r+") as file:
            data = load(file)
            if user_id not in data:
                self.bot.add_default()
            else:
                user_data = data[user_id]
                wins = user_data["wins"]
                losses = user_data["losses"]
            file.seek(0)
            dump(data, file)
            file.truncate()
        
        # print(f"---- {user.username} STATS ----\nYou have escaped {wins} times.\nYou have been caught {losses} times.")
        
        await self.bot.highrise.chat(f"---- {user.username} STATS ----\n{user.username} has escaped {wins} times.\nThey have been caught {losses} times.")
