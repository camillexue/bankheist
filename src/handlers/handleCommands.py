import importlib.util
import os
import json
import time

from highrise import User

def get_user_permissions(user:User):
    with open("config/permissions.json","r") as f:
        data = json.load(f)

    user_permissions = []

    for permission in data["permissions"]:
        if permission["username"] == user.username:
            user_permissions = permission["permissions"]
            break
        else:
            user_permissions = ["talk","play"]

    return user_permissions

def get_user_permissions_id(user_id):
    with open("config/permissions.json","r") as f:
        data = json.load(f)

    user_permissions = []

    for permission in data["permissions"]:
        if permission["user_id"] == user_id:
            user_permissions = permission["permissions"]
            break
        else:
            user_permissions = ["talk","play"]

    return user_permissions

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.commands = {}
        self.cooldowns = {}
        self.load_commands()

    def load_commands(self):
        """ Load commands from modules iin the src/commands directory"""
        commands_dir = os.path.join(
            os.path.dirname(__file__), "..", "commands")
        for category in os.listdir(commands_dir):
            category_dir = os.path.join(commands_dir, category)
            if os.path.isdir(category_dir):
                for command_file in os.listdir(category_dir):
                    if command_file.endswith(".py"):
                        command_name = os.path.splitext(command_file)[0] #command name same as file name
                        command_module = f"src.commands.{category}.{command_name}" #categories for commands
                        spec = importlib.util.spec_from_file_location(
                            command_module, os.path.join(category_dir, command_file)
                        )
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        command = getattr(module, "Command")(self.bot)
                        if command_name in self.commands:
                            del self.commands[command_name]
                            for alias in command.aliases:
                                if alias in self.commands:
                                    del self.commands[alias] # allow command alias
                        self.commands[command.name] = command 
                        if hasattr(command, "aliases"):
                            for alias in command.aliases:
                                self.commands[alias] = command 
    async def handlecommand(self, user, message):
        """ handle chat messages that start with prefix """
        parts = message[1:].split() # split prefix from the name
        if len(parts) < 1 or parts == []:
            return
        command_name = parts[0]
        args = parts[1:]
        command = self.commands.get(command_name)
        if command:
            if hasattr(command, "permissions"): # check perm
                user_permissions = get_user_permissions(user)
                if not all(p in user_permissions for p in command.permissions):
                    await self.bot.highrise.send_whisper(user.id, "You don't have permission to use this command.")
                    return
            cooldown = command.cooldown
            user_id = user.id
            if command_name in self.cooldowns and user_id in self.cooldowns[command_name]:
                remaining_time = self.cooldowns[command_name][user_id] - time.time()
                if remaining_time > 0:
                    await self.bot.highrise.send_whisper(user_id, f"{command_name} is on cooldown. Try again in {int(remaining_time)} seconds.")
                    return
            if command_name not in self.cooldowns:
                self.cooldowns[command_name] = {}
            self.cooldowns[command_name][user_id] = time.time() + cooldown
            await command.execute(user, args, message)


class CommandHandler_Whispers:
    def __init__(self, bot):
        self.bot = bot
        self.commands = {}
        self.cooldowns = {}
        self.load_commands()

    def load_commands(self):
        """ Load commands from modules iin the src/commands directory"""
        commands_dir = os.path.join(
            os.path.dirname(__file__), "..", "commands")
        for category in os.listdir(commands_dir):
            category_dir = os.path.join(commands_dir, category)
            if os.path.isdir(category_dir):
                for command_file in os.listdir(category_dir):
                    if command_file.endswith(".py"):
                        command_name = os.path.splitext(command_file)[0] #command name same as file name
                        command_module = f"src.commands.{category}.{command_name}" #categories for commands
                        spec = importlib.util.spec_from_file_location(
                            command_module, os.path.join(category_dir, command_file)
                        )
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        command = getattr(module, "Command")(self.bot)
                        if command_name in self.commands:
                            del self.commands[command_name]
                            for alias in command.aliases:
                                if alias in self.commands:
                                    del self.commands[alias] # allow command alias
                        self.commands[command.name] = command 
                        if hasattr(command, "aliases"):
                            for alias in command.aliases:
                                self.commands[alias] = command 
        
        whisper_commands_dir = os.path.join(
            os.path.dirname(__file__), "..", "whisper-commands")
        for category in os.listdir(whisper_commands_dir):
            category_dir = os.path.join(whisper_commands_dir, category)
            if os.path.isdir(category_dir):
                for command_file in os.listdir(category_dir):
                    if command_file.endswith(".py"):
                        command_name = os.path.splitext(command_file)[0] #command name same as file name
                        command_module = f"src.commands.{category}.{command_name}" #categories for commands
                        spec = importlib.util.spec_from_file_location(
                            command_module, os.path.join(category_dir, command_file)
                        )
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        command = getattr(module, "Command")(self.bot)
                        if command_name in self.commands:
                            del self.commands[command_name]
                            for alias in command.aliases:
                                if alias in self.commands:
                                    del self.commands[alias] # allow command alias
                        self.commands[command.name] = command 
                        if hasattr(command, "aliases"):
                            for alias in command.aliases:
                                self.commands[alias] = command 
    
    async def handlecommand(self, user, message):
        """ handle chat messages that start with prefix """
        parts = message[1:].split() # split prefix from the name
        if len(parts) < 1 or parts == []:
            return
        command_name = parts[0]
        args = parts[1:]
        command = self.commands.get(command_name)
        if command:
            if hasattr(command, "permissions"): # check perm
                user_permissions = get_user_permissions(user)
                if not all(p in user_permissions for p in command.permissions):
                    await self.bot.highrise.send_whisper(user.id, "You don't have permission to use this command.")
                    return
            cooldown = command.cooldown
            user_id = user.id
            if command_name in self.cooldowns and user_id in self.cooldowns[command_name]:
                remaining_time = self.cooldowns[command_name][user_id] - time.time()
                if remaining_time > 0:
                    await self.bot.highrise.send_whisper(user_id, f"{command_name} is on cooldown. Try again in {int(remaining_time)} seconds.")
                    return
            if command_name not in self.cooldowns:
                self.cooldowns[command_name] = {}
            self.cooldowns[command_name][user_id] = time.time() + cooldown
            await command.execute(user, args, message)

class CommandHandler_DMs:
    def __init__(self, bot):
        self.bot = bot
        self.commands = {}
        self.cooldowns = {}
        self.load_commands()

    def load_commands(self):
        """ Load commands from modules iin the src/commands directory"""
        commands_dir = os.path.join(
            os.path.dirname(__file__), "..", "dm-commands")
        for category in os.listdir(commands_dir):
            category_dir = os.path.join(commands_dir, category)
            if os.path.isdir(category_dir):
                for command_file in os.listdir(category_dir):
                    if command_file.endswith(".py"):
                        command_name = os.path.splitext(command_file)[0] #command name same as file name
                        command_module = f"src.commands.{category}.{command_name}" #categories for commands
                        spec = importlib.util.spec_from_file_location(
                            command_module, os.path.join(category_dir, command_file)
                        )
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        command = getattr(module, "Command")(self.bot)
                        if command_name in self.commands:
                            del self.commands[command_name]
                            for alias in command.aliases:
                                if alias in self.commands:
                                    del self.commands[alias] # allow command alias
                        self.commands[command.name] = command 
                        if hasattr(command, "aliases"):
                            for alias in command.aliases:
                                self.commands[alias] = command 
        
        whisper_commands_dir = os.path.join(
            os.path.dirname(__file__), "..", "dm-commands")
        for category in os.listdir(whisper_commands_dir):
            category_dir = os.path.join(whisper_commands_dir, category)
            if os.path.isdir(category_dir):
                for command_file in os.listdir(category_dir):
                    if command_file.endswith(".py"):
                        command_name = os.path.splitext(command_file)[0] #command name same as file name
                        command_module = f"src.commands.{category}.{command_name}" #categories for commands
                        spec = importlib.util.spec_from_file_location(
                            command_module, os.path.join(category_dir, command_file)
                        )
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        command = getattr(module, "Command")(self.bot)
                        if command_name in self.commands:
                            del self.commands[command_name]
                            for alias in command.aliases:
                                if alias in self.commands:
                                    del self.commands[alias] # allow command alias
                        self.commands[command.name] = command 
                        if hasattr(command, "aliases"):
                            for alias in command.aliases:
                                self.commands[alias] = command 
    
    async def handlecommand(self, user_id, convo_id, message):
        """ handle chat messages that start with prefix """
        parts = message[1:].split() # split prefix from the name
        if len(parts) < 1 or parts == []:
            return
        command_name = parts[0]
        args = parts[1:]
        command = self.commands.get(command_name)
        if command:
            if hasattr(command, "permissions"): # check perm
                user_permissions = get_user_permissions_id(user_id)
                if not all(p in user_permissions for p in command.permissions):
                    await self.bot.highrise.send_whisper(user_id, "You don't have permission to use this command.")
                    return
            cooldown = command.cooldown
            user_id = user_id
            if command_name in self.cooldowns and user_id in self.cooldowns[command_name]:
                remaining_time = self.cooldowns[command_name][user_id] - time.time()
                if remaining_time > 0:
                    await self.bot.highrise.send_whisper(user_id, f"{command_name} is on cooldown. Try again in {int(remaining_time)} seconds.")
                    return
            if command_name not in self.cooldowns:
                self.cooldowns[command_name] = {}
            self.cooldowns[command_name][user_id] = time.time() + cooldown
            await command.execute(user_id, convo_id, message)
                                                    
                                

                



