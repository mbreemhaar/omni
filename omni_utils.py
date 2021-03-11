from inspect import signature, iscoroutinefunction

# This module provides utility classes that enable simplified communication
# between the programmer and the Omni interface


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
        Inspects the callable in the instance's function field, calls the function
        depending on its signature, then returns the result.
        """

        func_signature = signature(self.function)
        params = func_signature.parameters

        arg_dict = {}

        if 'args' in params:
            arg_dict['args'] = arguments
        if 'message' in params:
            arg_dict['message'] = message

        if iscoroutinefunction(self.function):
            return await self.function(**arg_dict)
        else:
            return self.function(**arg_dict)


class OmniInterface():
    """
    Interface class that modules use to interact with the Omni architecture.
    """

    def __init__(self):
        # Commands being added are stored into the buffer until flush_buffers is called
        self.command_buffer = []
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
    
    def flush_buffers(self):
        """
        Currently this function only flushes the command buffer, but it will flush
        other buffers in the future. It flushes the buffers in such a way that
        if the methods that filled them have been replaced with the ones defined
        in omni.py, the buffers will be emptied. If this function is called
        prematurely however, the buffers stay intact.
        """

        old_commands = self.command_buffer
        self.command_buffer = []
        for command in old_commands:
            self.add_command(command)
