from highrise import User, Position

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'moveany'
        self.description = "move anyone anywhere"
        self.aliases = ["move", "anymove", "mv"]
        self.permissions = ["move-others"]
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        separated = message.split()
        coords = separated[-3:]
        
        if len(separated) <= 4:
            await self.bot.highrise.send_whisper(user.id, "Could not execute tp command.")
            return

        name = separated[1][1:]
        coords = separated[-3:]
        user_id_lookup = (await self.current_ids())
        invalid_coords = False
        for x in coords:
            if x.isalpha(): invalid_coords = True

        if name not in user_id_lookup.keys() or invalid_coords:
            # print(user_id_lookup.keys(),name)
            await self.bot.highrise.send_whisper(user.id,f"Could not teleport {name} to {coords}.")
            return
        else:
            name_id = user_id_lookup[name]
            try:
                await self.bot.highrise.teleport(name_id, Position (float(coords[0]) ,float(coords[1]) ,float(coords[2]) ,"FrontLeft"))

            except:
                await self.bot.highrise.send_whisper(user.id,f"Could not {name} teleport to {coords}.")

    async def current_ids(self):
        room_users = (await self.bot.highrise.get_room_users()).content
        usernames = {user[0].username: user[0].id for user in room_users}

        return usernames