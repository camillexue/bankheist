from highrise import User, Position

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'tp'
        self.description = "Moves player(s) to specific area "
        self.aliases = ["tp", "teleport"]
        self.permissions = ['move-others']
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        separated = message.split()
        destinations = {"jail": Position(14.5, 11.5, 1.5),
                        "roof":Position(14.5, 18.5, 23.5),
                        "sewers":Position(14.5, 0.5, 29.5),
                        "sewer-end":Position(3.5, 0.5, 5.5),
                        "airballoon":Position(3.5, 11.5, 5.5),
                        "police-roof":Position(14.5, 18.5, 2.5),
                        "secret":Position(11.5, 18.0, 10.5),
                        "vault":Position(15.5, 5.0, 29.5)
                }

        if len(separated) <= 2:
            await self.bot.highrise.send_whisper(user.id, "Could not execute tp command.")
            return
        name = separated[1][1:]
        location = separated[2]

        user_id_lookup = (await self.current_ids())
        
        if name not in user_id_lookup.keys() or location not in destinations.keys():
            # print(user_id_lookup.keys(),name)
            await self.bot.highrise.send_whisper(user.id,f"Could not teleport {name} to {location} zone.")
        else:
            name_id = user_id_lookup[name]
            position = destinations[location]
            try:
                await self.bot.highrise.teleport(name_id, position)
                await self.bot.sync_in_room()
            except:
                await self.bot.highrise.send_whisper(user.id,f"Could not {name} teleport to {location} zone.")

        

    async def current_ids(self):
        room_users = (await self.bot.highrise.get_room_users()).content
        usernames = {user[0].username: user[0].id for user in room_users}

        return usernames
    