# This module provides utility classes that enable simplified communication
# between the programmer and the Omni interface

"""
Basic command class.
"""
class Command():

    def __init__(self, function, handle,  help_message):
        self.handle = handle
        self.function = function
        self.help_message = help_message
