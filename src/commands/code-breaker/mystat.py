from highrise import User
from json import load, dump


class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'stats'
        self.description = "Your command description"
        self.aliases = ["me", "mystats", "tracker"]
        self.permissions = ['talk']
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):

        with open("./data.json", "r+") as file:
            data = load(file)
            if user.id not in data:
                self.bot.add_default_user()
            else:
                user_data = data[user.id]
                wins = user_data["wins"]
                losses = user_data["losses"]
            file.seek(0)
            dump(data, file)
            file.truncate()
        
        print(f"-----\n {user.username} STATS\nYou have escaped {wins} times.\nYou have been caught {losses} times.\n-----")
        
        await self.bot.whisper(user.id,f"---- {user.username} STATS ----\nYou have escaped {wins} times.\nYou have been caught {losses} times.")
       