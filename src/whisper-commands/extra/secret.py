from highrise import User, Position, Item

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'secret'
        self.description = "Moves player(s) to specific area "
        self.aliases = ["suprise", "easteregg","gift","cop","police"]
        self.permissions = ['talk']
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):

        
        try:
            outfit = (await self.bot.highrise.get_user_outfit(user.id)).outfit
            all_item_ids = [item.id for item in outfit]
            copshade_id = 'glasses-n_copgrab2019copshades'
            if copshade_id in all_item_ids:
                try:
                    await self.bot.highrise.send_whisper(user.id,"You look like a cop to me! You're allowed on the police station roof!")
                    await self.bot.highrise.teleport(user.id, Position(11.5, 18.0, 10.5))
                except:
                    await self.bot.highrise.send_whisper(user.id,f"Could not {user.id} teleport to secret zone.")
            else:
                await self.bot.highrise.send_whisper(user.id,"You're not allowed to do that. Maybe if you were disguised as a cop...")


        except:
            print("Could not execute command.")

        
    async def current_ids(self):
        room_users = (await self.bot.highrise.get_room_users()).content
        usernames = {user[0].username: user[0].id for user in room_users}

        return usernames
    



# Item(type='clothing', amount=1, id='glasses-n_copgrab2019copshades')