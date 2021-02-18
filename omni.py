import argparse
import importlib
import pkgutil
import warnings

import discord

import persistence
from omni_utils import Command

# Get bot token from running arguments
parser = argparse.ArgumentParser()
parser.add_argument('token', help='Your Discord bot token. (Make one at www.discord.com/developers)', type=str)
args = parser.parse_args()
token = args.token

# Discord client, used to interact with the discord API
client = discord.Client()

# Name of the package in which the bot's modules can be found
MODULE_PACKAGE = 'modules'

# Dictionary from lowercase strings to Command objects. Used to lookup the correct command
commands = {}

"""
An instance of this interface is placed in the 'omni' variable for each module 
that defines this variable, along with an 'init()' function. It enables limited 
interaction with certain objects in omni.py, such as adding commands or 
requesting to be updated when certain events occur.
"""
class OmniInterface():
    def __init__(self):
        self.client = client
    
    """
    Returns the command prefix used for the specified guild
    """
    def get_prefix(self, guild):
        return persistence.get_prefix(guild)

    """
    Add a command to the dictionary of commands.
    """
    def add_command(self, function, handle, help_message):
        new_command = Command(function, handle, help_message)
        if handle in commands:
            warnings.warn('The "{}" command is already defined.'.format(handle))
        commands[handle.lower()] = new_command


"""
Called whenever a command is used that could not be found
"""
def get_command_not_found_message(command, prefix):
    if command:
        return '"{}" is not a known command, type {}help for a list of available commands.'.format(command, prefix)
    else:
        return 'Please specify a command, type {}help for a list of available commands.'.format(prefix)


"""
Function that returns the help message attached to a specified command, or provides
a list of available commands.
"""
async def help_command(args, message):
    if not args:
        command_list = [command.handle for command in commands.values()]
        return 'These are the available commands:\n{}'.format('\n'.join(command_list))

    command = commands[args[0].lower()]
    if not command:
        return await get_command_not_found_message(command, persistence.get_prefix(message.guild))
    else:
        return command.help_message


"""
Function that sets the prefix for the guild in which the command was sent
"""
async def set_prefix_command(args, message):
    if not message.guild:
        return "I can only set the prefix for a server"

    if not args or args[0].isalnum() or len(args[0]) != 1:
        return "Please specify a single non-alphanumeric character such as ! or $"

    success = persistence.set_prefix(message.guild, args[0])

    if success:
        return 'The command prefix is now {}'.format(args[0])
    else:
        return 'Something went wrong while setting the command prefix.' + \
               'It remains "{}". Try again later.'.format(persistence.get_prefix(message.guild))



"""
Provides each module with an OmniInterface, and calls their init() function.
This function will recursively load all modules in the modules package.
"""
def __load_modules(package_name):
    package = __import__(package_name, fromlist=[" "])

    for _, modname, ispkg in pkgutil.iter_modules(package.__path__):

        if ispkg:
            __load_modules(package_name + '.' + modname)
        else:
            module = importlib.import_module('.' + modname, package_name)
            if hasattr(module, 'omni') and hasattr(module, 'init'):
                module.omni = OmniInterface()
                module.init()

# Add core commands to the command dictionary
commands['help'] = Command(help_command, 'help', 
'Use to receive help on how to use a command.')

commands['setprefix'] = Command(set_prefix_command, 'setPrefix', 
'Set the prefix used to indicate a command to a specified non-alphanumeric character such as ! or $')

# Load all modules before running the client
__load_modules(MODULE_PACKAGE)


################################################################################
#                                Client events                                 #
################################################################################

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    prefix = persistence.get_prefix(message.guild)
    if message.content.startswith(prefix):

        command_string = message.content.split()[0][len(prefix):]
        arguments = message.content.split()[1:]
        command = commands.get(command_string.lower(), None)

        if command:
            response = await command.function(arguments, message)
        else:
            response = get_command_not_found_message(command_string, prefix)

        if response:
            await message.channel.send(response)
    
# Finally, start the bot by running the client
client.run(token)
