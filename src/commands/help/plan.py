from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'plan'
        self.description = "When a player tries to play"
        self.aliases = ["howtoplay", "play","how"]
        self.permissions = ['talk']
        self.cooldown = 30

    async def execute(self, user: User, args: list, message: str):
        if user.id == "62fb30c5132e425314f6758f":
            await self.bot.highrise.chat("1. Climb into the roof vent (Find the teleporter)\n2. Walk to the vault\n3. Crack the vault code with /enter")
            await self.bot.highrise.chat("4. Rob the bank and enter the sewers (Find the teleporter)\n5. Navigate the sewers (Don't get seen by @PatrolBot)\n 6. Get to the escape air balloon!")
        else:    
            await self.bot.whisper(user.id,"Ready to start the heist? Here's the plan. I'll disable the security system, and you will: ")
            await self.bot.whisper(user.id,"1. Climb into the roof vent (Find the teleporter)\n2. Walk to the vault\n3. Crack the vault code with /enter")
            await self.bot.whisper(user.id,"4. Rob the bank and enter the sewers (Find the teleporter)\n5. Navigate the sewers (Don't get seen by @PatrolBot)\n 6. Get to the escape air balloon!")

