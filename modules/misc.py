from omni_utils import OmniInterface
from omni_events import MessageDeletedEvent, ReactionAddedEvent, ReactionRemovedEvent
omni = OmniInterface()


@omni.command('ping', 'Test command to check if the bot is alive')
def ping():
    """
    Test command to check if the bot is alive. The bot should respond with 'pong'
    in the chat in which the command was sent.
    """

    return 'pong'

async def precious_deleted(channel):
    await channel.send(":(")

@omni.command('precious', 'Test command to see if subscriptions work. Sends a message and will respond if it is deleted.')
async def precious(channel):
    message = await channel.send("Don't delete this!")
    event = MessageDeletedEvent(message)
    omni.subscribe(event, precious_deleted)

async def reaction_added(user, channel):
    await channel.send('<@{}> added a reaction'.format(user.id))

async def reaction_removed(user, channel):
    await channel.send('<@{}> removed a reaction'.format(user.id))

@omni.command('reactionTest', 'Test command to see if subscriptions work. Sends a message and will respond if a reaction is added or removed')
async def friends(channel):
    message = await channel.send("React to this message!")
    
    add_event = ReactionAddedEvent(message)
    omni.subscribe(add_event, reaction_added)

    remove_event = ReactionRemovedEvent(message)
    omni.subscribe(remove_event, reaction_removed)