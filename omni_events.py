from abc import ABC, abstractmethod, abstractstaticmethod
import discord

class Event(ABC):

    def __init__(self, discord_object):
        for discord_class in self.can_happen_to():
            if isinstance(discord_object, discord_class):
                self.discord_object = discord_object
                return
        raise TypeError(
        """
        An event of type {} cannot be created for an object of type {}.
        """.format(type(self), type(discord_object)))

    @abstractstaticmethod
    def can_happen_to():
        pass
    
    @abstractstaticmethod
    def get_relevant_ids(discord_object):
        pass

class MessageSentEvent(Event):

    @staticmethod
    def can_happen_to():
        return(
            discord.abc.User, discord.Guild, discord.TextChannel, 
            discord.DMChannel, discord.GroupChannel
        )

    @staticmethod
    def get_relevant_ids(message):
        return (message.author.id, message.channel.id, message.guild.id)

class MessageDeletedEvent(Event):

    @staticmethod
    def can_happen_to():
        return(
            discord.Message, discord.Guild, discord.TextChannel, 
            discord.DMChannel, discord.GroupChannel
        )

    @staticmethod
    def get_relevant_ids(message):
        return (message.id, message.channel.id, message.guild.id)

class MessageEditedEvent(Event):
    @staticmethod
    def can_happen_to():
        return(
            discord.Message, discord.Guild, discord.TextChannel, 
            discord.DMChannel, discord.GroupChannel
        )

    @staticmethod
    def get_relevant_ids(message):
        return (message.id, message.channel.id, message.guild.id)
