from enum import Enum
import discord
# This module provides utility classes that enable simplified communication
# between the programmer and the Omni interface

class Event(Enum):
    MESSAGE = 'MESSAGE'
    MESSAGE_DELETED = 'MESSAGE_DELETED'
    MESSAGE_EDITED = 'MESSAGE_EDITED'

    @staticmethod
    def is_compatible(discord_object, event):
        compatibility = {
        Event.MESSAGE : (discord.abc.User, discord.Guild, discord.TextChannel, 
        discord.DMChannel, discord.GroupChannel),

        Event.MESSAGE_DELETED : (discord.Message, discord.Guild, 
        discord.TextChannel, discord.DMChannel, discord.GroupChannel),

        Event.MESSAGE_EDITED : (discord.Message, discord.Guild, 
        discord.TextChannel, discord.DMChannel, discord.GroupChannel)
        }

        compatible_classes = compatibility.get(event, [])
        compatible_types = [c.__name__ for c in compatible_classes]

        for discord_class in compatible_classes:
            if isinstance(discord_object, discord_class):
                return True, compatible_types
        
        return False, compatible_types

class Command():
    """
    Basic command class.
    """

    def __init__(self, function, handle,  help_message):
        self.handle = handle
        self.function = function
        self.help_message = help_message


class Subscription():

    def __init__(self, discord_object, create_function = None):
        if not hasattr(discord_object, 'id'):
            raise TypeError("""A subscription was created for object:\n
            {}\n
            Of type: {}\n
            This object does not have an id attribute, and hence the subscription 
            is not valid.""".format(discord_object, type(discord_object)))
        
        self.discord_object = discord_object

        self.create_function = create_function
        self.event_dict = {}
    
    def __getitem__(self, event):
        return self.event_dict.get(event, None)
    
    def __setitem__(self, event, event_function):
        compatible, compatible_types = Event.is_compatible(self.discord_object, event)
        if not compatible:
            raise TypeError("""
            A function for event {} is being implemented in a subscription for 
            an object with type {}, but the event is only compatible with 
            objects of type:\n{}
            """.format(event, type(self.discord_object), compatible_types))
        self.event_dict[event] = event_function



class OmniInterface():
    """
    Interface class that modules use to interact with the Omni architecture.
    """

    def __init__(self):
        # Commands being added are stored into the buffer until flush_buffers is called
        self.command_buffer = []
        self.subscription_buffer = []
        self.module_name = None

    def add_command(self, command):
        """
        Add a Command object to the bot's commands. Initially this method adds
        the command to the command buffer, but during startup it is replaced by
        one that adds the command directly to the bot's commands.
        """

        self.command_buffer.append(command)
   
    def command(self, handle, help_message):
        """
        Command decorator. Add this decorator to a function in order to indicate
        that it should be added to the bot's commands.
        """

        def add_command_wrapper(function):
            command = Command(function, handle, help_message)
            self.add_command(command)

            # Return the function, in order to not affect it in its original module
            return function

        # Return the wrapper, which is instantly called
        return add_command_wrapper
    
    def add_subscription(self, subscription):
        self.subscription_buffer.append(subscription)

    def subscribe(self, discord_object, create_function = None):
        sub = Subscription(discord_object, create_function)
        self.add_subscription(sub)
        return sub


    def flush_buffers(self):
        """
        Flushes the command and subscription buffers. 
        It flushes the buffers in such a way that if the methods that filled 
        them have been replaced with the ones defined in omni.py, the buffers 
        will be emptied. If this function is called prematurely however, 
        the buffers stay intact.
        """

        old_commands = self.command_buffer
        self.command_buffer = []
        for command in old_commands:
            self.add_command(command)
        
        old_subscriptions = self.subscription_buffer
        self.subscription_buffer = []
        for subscription in old_subscriptions:
            self.add_subscription(subscription)


