from inspect import signature, iscoroutinefunction

# This module provides utility classes that enable simplified communication
# between the programmer and the Omni interface

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



class Command():
    """
    Basic command class.
    """

    def __init__(self, function, handle,  help_message):
        self.handle = handle
        self.function = function
        self.help_message = help_message
    
    async def execute(self, arguments, message):
        """
        Does a fluid call on the command function.
        """
        arg_dict = {
            'args':arguments,
            'message':message,
            'channel':message.channel,
            'guild':message.guild,
            'author':message.author
        }
        return await fluid_call(self.function, arg_dict)


class Subscription():

    def __init__(self, discord_object, create_function = None):
        if not hasattr(discord_object, 'id'):
            raise TypeError("""A subscription was created for object:\n
            {}\n
            Of type: {}\n
            This object does not have an id attribute, and hence the subscription 
            is not valid.""".format(discord_object, type(discord_object)))
        
        self.id = discord_object.id
        self.create_function = create_function
        self.create()
    
    def create(self):
        if self.create_function:
            self.create_function(self)


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


