from highrise import User, Position

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'refresh'
        self.description = "move anyone anywhere"
        self.aliases = ["reload", "anymove", "mv"]
        self.permissions = ["host", "moderate"]
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        try:
            await self.bot.sync_in_room()
        except:
            print("ErrorCould not reload positions in room.")