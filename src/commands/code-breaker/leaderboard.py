from highrise import User
import random
from highrise.models import Item, Position, AnchorPosition
from json import load,dump

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'leaderboard'
        self.description = "User gets their game info"
        self.aliases = ["top", "top5"]
        self.permissions = ["talk"]
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        separated = message.split()

        username_lookup = (await self.bot.in_room_names_dict())


        with open("./data.json", "r+") as file:
            data = load(file)
            total_winners = 0
            total_losses = 0

            sorted_users = sorted(data, key=self.getWins, reverse=True)
            top_five = sorted_users[:5]
            # print(top_five)
            top5_usernames = [data[x]["username"] for x in top_five]

            combined = [ f"{top_five.index(x)+1}. " + data[x]["username"] + " " + str(data[x]["wins"]) +" escapes" for x in top_five]

            for player in data:
                wins = data[player]["wins"]
                losses = data[player]["losses"]
                if wins > 0:
                    total_winners += 1
                total_losses += losses
            file.seek(0)
            dump(data, file)
            file.truncate()
        
        await self.bot.whisper( user.id,"------------\nBANK HEIST STATS\n" + 
                                f"\n".join(combined) +"\n------------")
        await self.bot.whisper( user.id,f"{total_winners} out of {len(data)} players have completed at least one heist successfully! Players have been caught {total_losses} times combined.")


    def getWins(self, elem):
        with open("./data.json", "r+") as file:
            data = load(file)
            file.seek(0)
        return data[elem]["wins"]