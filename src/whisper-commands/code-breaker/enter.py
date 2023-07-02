from highrise import User
import random
from highrise.models import Item, Position, AnchorPosition
import asyncio


class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'enter'
        self.description = "Your command description"
        self.aliases = ["try", "guess", "attempt","code","e"]
        self.permissions = ["play"]
        self.cooldown = 0

    async def execute(self, user: User, args: list, message: str):
        jail_pos = Position(14.5, 11.5, 1.5)
        separated = message.split()
        if user.id not in self.bot.user_info:
            if not await self.bot.check_save(user):
                await self.bot.add_default_user(user)
        
        user_data = self.bot.user_info[user.id]
        if user_data["game_stage"] > 2:
            await self.bot.whisper(user.id,"You are not in the code-breaking stage! /replay to play again")
            print(user_data["location"])
            return
        
        if user_data["location"] != "out-vault":
            await self.bot.whisper(user.id,"You're too far from the vault door to enter the code! Find a way to the vault! \nUse /replay if you are stuck to start again.")
            print(user_data["location"])
            return
        
        

        if len(separated) <= 1 or len(separated) >=3:
            await self.bot.whisper(user.id,"Invalid code input. Use the format: \n/enter 1234")
            return
        if len(separated[1]) != 4 or not separated[1].isdigit():
            await self.bot.whisper(user.id,"Invalid code input. Use the format: \n/enter 1234")
        else:
            await self.bot.whisper(user.id,f"You have entered: {separated[1]}")
            await self.code_break(user_data, separated[1])
        
        await self.bot.save_data()


    async def code_break(self, data, input_code):
        attempt_count = data["code_attempts"]    
        answer_code = data["answer_code"] 
        user_id = data["user_id"]
        user_name = data["username"]
        partial = ''
        max_attempts = 11


        if answer_code == 'XXXX': # if no current code to guess
            answer_code = random.randrange(1000, 10000) # set new code
            print(f"{user_name}'s Answer Code is: {answer_code}")
            self.bot.user_info[user_id]["answer_code"] = answer_code
        
        if int(input_code) == answer_code: # entered correct code
            try:
                await self.bot.highrise.teleport(user_id, Position(13.5, 5.0, 29.5))
                await self.bot.whisper(data["user_id"],f"\U00002705 YES! YOU'RE IN. {input_code} WAS CORRECT! \n*You grab as much gold as you can fit in your pockets*\U0001F4B0\U0001F4B0\U0001F4B0")
                await self.bot.whisper(data["user_id"],f"We blew a hole in the floor that connects to the sewers.") 
                await self.bot.whisper(data["user_id"],f"Climb down the ladder! (Find the teleporter)")
                self.bot.user_info[user_id]["answer_code"] = 'XXXX' #reset guess code for next time
                self.bot.user_info[user_id]["game_stage"] = 3
                self.bot.user_info[user_id]["current_code"] = 'XXXX'
                self.bot.user_info[user_id]["code_attempts"] = 0
                self.bot.user_info[user_id]["eliminated_digits"] = [] 
                self.bot.user_info[user_id]["location"] = 'in-vault'
                await self.bot.save_data() 
            except Exception as e:
                print(f"Caught Teleport Error: {e}")

        # If code enter is not correct: 
        else:
            input_code = str(input_code)
            answer_code = str(answer_code)
            correct_count = 0
            # correct[] list stores digits which are correct
            correct = ['X']*4
            partial = ''.join(set(input_code).intersection(answer_code))
            elim = set(input_code) - set(answer_code)
            old = self.bot.user_info[user_id]["eliminated_digits"]
            combined = (set(old)).union(elim)
            self.bot.user_info[user_id]["eliminated_digits"] = list(combined)
            # for loop runs 4 times since the number has 4 digits.
            for i in range(0, 4):
                # checking for equality of digits
                if (input_code[i] == answer_code[i]):
                    # number of digits guessed correctly increments
                    correct_count += 1
                    # hence, the digit is stored in correct[].
                    correct[i] = answer_code[i]
                
                else:
                    continue
            data["code_attempts"] += 1
            all_elims = ', '.join(sorted(combined))
            remaining_attempts = max_attempts - (attempt_count + 1)

            if partial == '':
                await self.bot.whisper(user_id,f"Oop! None of those numbers are in the vault code. \nRemaining Attempts: {remaining_attempts}")
                if data["code_attempts"] >= 7 and data["code_attempts"] < max_attempts:
                    await self.bot.whisper(user_id,f"Here's a hint! None of these digits are in the code: {all_elims}")
                if data["code_attempts"] >= 12:
                    await self.bot.whisper(user_id,f"Oh no! It took you too many attempts to break the vault code!! You got caught! Use /replay to start the game again.")
                    try:
                        await self.bot.highrise.teleport(user_id, self.bot.jail_pos)
                        self.bot.user_info[user_id]["answer_code"] = 'XXXX' #reset guess code for next time
                        self.bot.user_info[user_id]["game_stage"] = 0
                        self.bot.user_info[user_id]["losses"] += 1
                        self.bot.user_info[user_id]["current_code"] = 'XXXX'
                        self.bot.user_info[user_id]["code_attempts"] = 0
                        self.bot.user_info[user_id]["eliminated_digits"] = [] 
                        self.bot.user_info[user_id]["location"] = 'jail' 
                        await self.bot.save_data() 
                    except Exception as e:
                        print(f"Caught Teleport Error: {e}")
            else:
                await self.bot.whisper(user_id,f"The digit(s) {partial} are correct, and these were in the correct position: {''.join(correct)}\nRemaining Attempts: {remaining_attempts}")
                if data["code_attempts"] >= 7 and data["code_attempts"] < max_attempts:
                    await self.bot.whisper(user_id,f"Here's a hint! None of these digits are in the code: {all_elims}")

                if data["code_attempts"] >= max_attempts:
                    await self.bot.whisper(user_id,f"Oh no! It took you too many attempts to break the vault code!! You got caught! The correct code was {answer_code}. \nUse /replay to start the game again.")
                    await self.bot.highrise.chat(f"\U0001F6A8 {user_name} WAS CAUGHT!\U0001F6A8\nThey got sent to jail.")
                    try:
                        await self.bot.highrise.teleport(user_id, self.bot.jail_pos) 
                        self.bot.user_info[user_id]["answer_code"] = 'XXXX' #reset guess code for next time
                        self.bot.user_info[user_id]["game_stage"] = 0
                        self.bot.user_info[user_id]["losses"] += 1
                        self.bot.user_info[user_id]["current_code"] = 'XXXX'
                        self.bot.user_info[user_id]["code_attempts"] = 0
                        self.bot.user_info[user_id]["eliminated_digits"] = [] 
                        self.bot.user_info[user_id]["location"] = 'jail' 
                        await self.bot.save_data() 
                    except Exception as e:
                        print(f"Caught Teleport Error: {e}")
            # print("Eliminated Digits:",self.bot.user_info[user_id]["eliminated_digits"])
            data["current_code"] = "".join(correct)   
            self.bot.user_info[user_id] = data

        