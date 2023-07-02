from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'commands'
        self.description = "List of commands"
        self.aliases = ["list"]
        self.permissions = ['talk']
        self.cooldown = 30

    async def execute(self, user: User, args: list, message: str):
        await self.bot.whisper(user.id,"---- COMMANDS ---\n/replay - restart the game \n/help - game info \n/plan - heist plan steps \n/me - your stats")
        await self.bot.whisper(user.id,"/enter - attempt to solve the vault code, for example: \n@HeistBot /enter 9870\nthis command must be whispered.")