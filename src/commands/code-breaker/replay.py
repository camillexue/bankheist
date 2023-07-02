from highrise import User
import random
from highrise.models import Item, Position, AnchorPosition


class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'replay'
        self.description = "Your command description"
        self.aliases = ["resetgame", "restart", "redo"]
        self.permissions = ["play"]
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):

        if user.id not in self.bot.user_info:
            if not await self.bot.check_save(user):
                await self.bot.add_default_user(user)
        
        user_data = self.bot.user_info[user.id]
        self.bot.user_info[user.id]["game_stage"] = 0
        self.bot.user_info[user.id]["answer_code"] = 'XXXX'
        self.bot.user_info[user.id]["current_code"] = 'XXXX'
        self.bot.user_info[user.id]["code_attempts"] = 0
        self.bot.user_info[user.id]["eliminated_digits"] = []       
        
        try:
            await self.bot.highrise.teleport(user.id, Position (13.5, 18.5 ,27.5))
            self.bot.user_info[user.id]["location"] = 'roof'
        except Exception as e:
            print(f"Caught teleport Error: {e}")
        
        await self.bot.save_data()
