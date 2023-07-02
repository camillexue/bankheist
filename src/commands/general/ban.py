from highrise import User, Position

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'ban'
        self.description = "ban user "
        self.aliases = ['Ban', 'BAN']
        self.permissions = ["moderate"]
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        #separete message into parts
        parts = message.split()
        username_to_ids = await self.current_ids()
        #check if message is valid "ban @username"
        if len(parts) != 2:
            await self.bot.highrise.send_whisper(user.id, "Invalid ban command format.")
            return
        await self.ban_user(message,user,username_to_ids)

    async def ban_user(self, message: str, user: User, username_to_id: dict):
        parts = message.split()
        username = parts[1][1:]
        #check if user is in room
        if username in username_to_id.keys():
            #get user id
            user_id = username_to_id[username]
            # print(f"{username} found, id: {type(user_id)}")
            try:
                #mute user
                await self.bot.highrise.moderate_room(user_id, "ban")
                #send message to chat
                await self.bot.highrise.send_whisper(user.id,f"{username} has been banned.")
            except:
                await self.bot.highrise.send_whisper(user.id,f"{username} could not be banned.")
        else:
            await self.bot.highrise.send_whisper(user.id,f"{username} could not be banned.")

    async def check_for_user_in_room(self, user, username: str, username_to_id: dict):
        if username not in username_to_id.keys():
            #check if user is in room
            room_users = (await self.bot.highrise.get_room_users()).content
            for room_user, pos in room_users:
                if room_user.username == username:
                    username_to_id[username] = room_user.id
                    print(f"Added {username} to username_to_id")
                    return 1         
            if username not in username_to_id.keys():    
                await self.bot.highrise.send_whisper(user.id,"User not found.")
                return 0

    async def current_ids(self):
        room_users = (await self.bot.highrise.get_room_users()).content
        usernames = {user[0].username: user[0].id for user in room_users}
        # print(usernames)

        return usernames