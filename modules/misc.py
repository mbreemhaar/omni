from omni_utils import OmniInterface
omni = OmniInterface()


@omni.command('ping', 'Test command to check if the bot is alive')
def ping():
    """
    Test command to check if the bot is alive. The bot should respond with 'pong'
    in the chat in which the command was sent.
    """

    return 'pong'
