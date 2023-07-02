from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'win'
        self.description = "Your command description"
        self.aliases = []
        self.permissions = ['talk']
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        await self.bot.whisper(user.id,"If I didn't register your win, take a pic in the air balloon and use #BankHeist so @SpillyMilly can see that you escaped!")


