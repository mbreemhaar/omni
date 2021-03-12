from omni_utils import OmniInterface
from omni_events import MessageDeletedEvent
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

@omni.command('precious', 'Test command to see if subscriptions work')
async def precious(channel):
    message = await channel.send("Don't delete this!")
    event = MessageDeletedEvent(message)
    omni.subscribe(event, precious_deleted)