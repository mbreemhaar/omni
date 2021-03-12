import argparse
import importlib
import pkgutil
import warnings
import types
import asyncio
from inspect import signature, iscoroutinefunction

import discord

import persistence
from omni_utils import OmniInterface
from omni_events import *

# Get bot token and Mongo address/port from running arguments
parser = argparse.ArgumentParser()
parser.add_argument('token', help='Your Discord bot token. (Make one at www.discord.com/developers)', type=str)
args = parser.parse_args()

token = args.token

# Initialize Discord client, used to interact with the discord API
intents = discord.Intents().default()
intents.members = True
client = discord.Client(intents=intents)

# Name of the package in which the bot's modules can be found
MODULE_PACKAGE = 'modules'

# Dictionary from lowercase strings to Command objects. Used to lookup the correct command
commands = {}

# Dictionary from Discord object id's to a list of Subscription objects
subscriptions = {}

# List of the interfaces that are loaded during startup
interfaces = []

# The core interface in which commands are defined that require direct access
# to attributes of this module
core_interface = OmniInterface()
core_interface.module_name = 'omni core'
interfaces.append(core_interface)

def get_command_not_found_message(command, prefix):
    """
    Called whenever a command is used that could not be found
    """

    if command:
        return '"{}" is not a known command, type {}help for a list of available commands.'.format(command, prefix)
    else:
        return 'Please specify a command, type {}help for a list of available commands.'.format(prefix)

# Add core commands to the core interface

@core_interface.command('help', 'Use to receive help on how to use a command.')
def help_command(args, message):
    """
    Function that returns the help message attached to a specified command,
    or provides a list of available commands.
    """

    if not args:
        command_list = [command.handle for command in commands.values()]
        return 'These are the available commands:\n{}'.format('\n'.join(command_list))

    command = commands[args[0].lower()]
    if not command:
        return get_command_not_found_message(command, persistence.get_prefix(message.guild))
    else:
        return command.help_message


@core_interface.command('setPrefix', 'Set the prefix used to indicate a command \
to a specified non-alphanumeric character such as ! or $')
def set_prefix_command(args, message):
    """
    Function that sets the prefix for the guild in which the command was sent
    """

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


@core_interface.command('getPrefix', 'Show the command prefix that Omni will currently respond to.')
def get_prefix_command(message):
    """
    Function that retrieves the prefix for the guild in which the command was sent
    """

    if not message.guild:
        return "I can only retrieve the prefix for a server"
    
    prefix = persistence.get_prefix(message.guild)
    
    response = "I am currently responding to the following prefix: {}".format(prefix)

    if message.content.startswith(prefix):
        response += "\nBut you already knew that, it seems..."

    return response

def interface_get_prefix(self, guild):
    """
    Function that is added to interfaces, in order to provide them with a means
    of retrieving the prefix associated with a guild
    """

    return persistence.get_prefix(guild)

def interface_add_command(self, command):
    """
    Function that replaces the add_command function of an interface to enable
    adding a command at run time
    """

    if commands.get(command.handle, None):
        warnings.warn(
        """Command with handle '{}' is being added by module with name '{}', 
        but it already existed. New command was not added""".format(command.handle, self.module_name))
    commands[command.handle.lower()] = command

def interface_add_subscription(self, subscription):
    if not subscriptions.get(subscription.id, None):
        subscriptions[subscription.id] = []
    subscriptions[subscription.id].append(subscription)


def __load_modules(package_name):
    """
    Retrieves the interface from each module and adds it to the interfaces list,
    also provides each interface with a name referring to the module it came from
    """

    package = __import__(package_name, fromlist=[" "])
    for _, modname, ispkg in pkgutil.iter_modules(package.__path__):

        if ispkg:
            __load_modules(package_name + '.' + modname)
        else:
            module = importlib.import_module('.' + modname, package_name)
            if hasattr(module, 'omni'):
                interface = module.omni
                interfaces.append(interface)
                interface.module_name = package_name

def __init_interfaces():
    """
    Provides each interface with a means of updating the collections in this
    module, and functions to query global variables.
    """

    for interface in interfaces:
        interface.get_prefix = types.MethodType(interface_get_prefix, interface)
        interface.add_command = types.MethodType(interface_add_command, interface)
        interface.add_subscription = types.MethodType(interface_add_subscription, interface)
        interface.flush_buffers()

# Load all modules and initialize their interfaces before running the client
__load_modules(MODULE_PACKAGE)
__init_interfaces()

################################################################################
#                                Client events                                 #
################################################################################

async def fluid_call(callable_object, arg_dict):
    object_signature = signature(callable_object)
    object_parameters = [param for param in object_signature.parameters]

    provided_params = arg_dict.keys()

    final_args = {}
    for param in provided_params:
        if param in object_parameters:
            final_args[param] = arg_dict[param]
            object_parameters.remove(param)
    
    if object_parameters:
        raise TypeError("""Error in fluid call:\n Callable {} requires the 
        following arguments that were not provided:\n{}
        """.format(callable_object, object_parameters))
    
    if iscoroutinefunction(callable_object):
        return await callable_object(**final_args)
    else:
        return callable_object(**final_args)

async def delegate_event(event_class, relevant_ids, arg_dict):
    for relevant_id in relevant_ids:
        for sub in subscriptions.get(relevant_id, []):
            if not isinstance(sub.event, event_class):
                continue
            function = sub.function
            call = fluid_call(function, arg_dict)
            asyncio.create_task(call)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    arg_dict = {
        'message':message,
        'channel':message.channel,
        'guild':message.guild,
        'author':message.author
    }

    e = MessageSentEvent
    await delegate_event(e, e.get_relevant_ids(message), arg_dict)

    if message.author == client.user:
        return
    
    # The command prefix for the guild that the message was sent in
    prefix = persistence.get_prefix(message.guild)

    # The string indicating that the bot is being mentioned. e.g. '@Omni' in the
    # discord client.
    mention = "<@!{}>".format(client.user.id)

    content = message.content

    # The string representing the command, and the arguments following it are
    # extracted differently depending on how the bot is addressed
    if content.startswith(mention):
        # If the bot is addressed by starting the message with mentioning it,
        # the command string is interpreted to be the first word in the message
        # after the mention
        after_mention = content[len(mention):].lstrip()
        command_string = after_mention.split()[0]
        arguments = after_mention.split()[1:]
    elif content.startswith(prefix):
        # If the bot is addressed by the guild's prefix, the command string is
        # interpreted to be the first word in the message, minus the prefix.
        command_string = content.split()[0][len(prefix):]
        arguments = content.split()[1:]
    else:
        return
    
    arg_dict['args'] = arguments
    command = commands.get(command_string.lower(), None)

    if command:
        response = await fluid_call(command.function, arg_dict)
    else:
        response = get_command_not_found_message(command_string, prefix)

    if response:
        await message.channel.send(response)

@client.event
async def on_message_delete(message):
    arg_dict = {
        'message':message,
        'channel':message.channel,
        'guild':message.guild,
        'author':message.author
    }

    e = MessageDeletedEvent
    await delegate_event(e, e.get_relevant_ids(message), arg_dict)

@client.event
async def on_reaction_add(reaction, user):
    arg_dict = {
        'reaction': reaction,
        'user': user,
        'message': reaction.message,
        'channel': reaction.message.channel,
        'guild' : reaction.message.guild,
        'author' : reaction.message.author
    }

    e = ReactionAddedEvent
    await delegate_event(e, e.get_relevant_ids(reaction, user), arg_dict)

@client.event
async def on_reaction_remove(reaction, user):
    arg_dict = {
        'reaction': reaction,
        'user': user,
        'message': reaction.message,
        'channel': reaction.message.channel,
        'guild' : reaction.message.guild,
        'author' : reaction.message.author
    }

    e = ReactionRemovedEvent
    await delegate_event(e, e.get_relevant_ids(reaction, user), arg_dict)


# Finally, start the bot by running the client
client.run(token)
