# This module provides utility classes that enable simplified communication
# between the programmer and the Omni interface


class Subscription():
    def __init__(self, event, function):
        self.event = event
        self.id = event.discord_object.id
        self.function = function

class Command():
    """
    Basic command class.
    """

    def __init__(self, function, handle,  help_message):
        self.handle = handle
        self.function = function
        self.help_message = help_message


class OmniInterface():
    """
    Interface class that modules use to interact with the Omni architecture.
    """

    def __init__(self):
        # Commands being added are stored into the buffer until flush_buffers is called
        self.command_buffer = []
        self.subscription_buffer = []
        self.message_buffer = []
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

    def subscribe(self, event, function):
        subscription = Subscription(event, function)
        self.add_subscription(subscription)

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


