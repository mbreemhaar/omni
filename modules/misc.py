omni = None

def init():
    omni.add_command(ping, 'ping', 'Check if the bot is alive')


"""
Test command to check if the bot is alive
"""
async def ping(args, message):
    return 'pong'