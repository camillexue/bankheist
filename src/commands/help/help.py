from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'help'
        self.description = "Your command description"
        self.aliases = ["Help", "how", "How","hint","Hint"]
        self.permissions = ['talk']
        self.cooldown = 3

    async def execute(self, user: User, args: list, message: str):

        if user.id not in self.bot.user_info:
            if not await self.bot.check_save(user):
                await self.bot.add_default_user(user)
        try: 
            position = await self.bot.check_position(user.id)
            # print(position)
            location = await self.bot.get_location_from_pos(user.id, position)
            match location:
                case 'roof':
                    await self.bot.whisper(user.id,"There's a hidden teleporter on the roof to get into the bank. Try tapping under the vent!")
                case 'sewers':
                    await self.bot.whisper(user.id,"Don't touch the spikes! Careful there's hidden spikes at the very end corner. Maybe tap a little to the left of where you think you should tap... ")
                case 'bank':
                    await self.bot.whisper(user.id,"You can walk to the vault from there! Just tap in front of the vault door to walk down.")
                case 'out-vault':
                    await self.bot.whisper(user.id,"Everyone has a different 4-digit code to get in. Take a guess by whispering a 4 digit number to @HeistBot. \nSay @HeistBot at the start of your message to whisper")
                case 'in-vault':
                    await self.bot.whisper(user.id,"Find the hidden teleporter to climb down the ladder! It's close to the ladder... maybe under something...")
                case 'sewers-II':
                    await self.bot.whisper(user.id,"Patrol Bot can't see you when you're hiding along the right wall. He also can't see anything behind him!")
                case 'airballoon':
                    await self.bot.whisper(user.id,"Congrats on escaping! If I didn't register your win, post a pic with #BankHeist with you in the air balloon so @SpillyMilly can see it!")
                    await self.bot.whisper(user.id,"The current prize is: 100G to the first 100 people that escape!")
                case 'jail':
                    await self.bot.whisper(user.id,"To get out of jail, say /replay to start over. I'll send you back to roof of the bank!")
                case 'jail-roof':
                    await self.bot.whisper(user.id,"Say /replay to play again and climb the \n/leaderboard")
                case 'wandering':
                    await self.bot.whisper(user.id,"Say /replay to play again and climb the \n/leaderboard")
                    await self.bot.whisper(user.id,"There's a /secret way to get onto the roof of the police station. Can you figure it out?")

                case  other:
                    await self.bot.whisper(user.id,"Say /replay to play again and climb the \n/leaderboard")
                    await self.bot.whisper(user.id,"There's a /secret way to get onto the roof of the police station. Can you figure it out?")

        except Exception as e:
            print(f"Caught Error when executing command for {user.username}: {e}")



