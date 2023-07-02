from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'info'
        self.description = "Your command description"
        self.aliases = ["bankheist", "hmm", "heist", "game"]
        self.permissions = ['talk']
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        await self.bot.whisper(user.id,"This is Bank Heist, a bot-driven escape game experience!")
        await self.bot.whisper(user.id,"Crack the code for the bank vault and then run through the sewers to get to the escape air balloon!")
        await self.bot.whisper(user.id,"Be careful! If you get caught, you'll be sent to jail and have to /replay to start over.")
        await self.bot.whisper(user.id,"Still confused? Use /plan or /commands")


