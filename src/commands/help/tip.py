from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'tip'
        self.description = "Your command description"
        self.aliases = ["prize", "gold"]
        self.permissions = ['talk']
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        await self.bot.whisper(user.id,"This game is just for fun! But @SpillyMilly is tipping 100G to the first 100 people that successfully escape")
        await self.bot.whisper(user.id,"as a thank you for helping her work out the bot bugs!")


