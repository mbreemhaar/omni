import random

# This field will contain an OmniInterface object when init() is called
omni = None

"""
init is used to initialize the commands specified in this module, using the
interface that was placed in the omni variable before init() is called
"""
def init():
    omni.add_command(roll, 'roll', 'Rolls a 6-sided die, or an n-sided die if an integer n is provided')
    omni.add_command(marco_polo, 'marco', "He'll be fine")

"""
Test command to see if the bot is alive
"""
async def marco_polo(args, message):
    return 'POLO!'

"""
Command to roll a die
"""
async def roll(args, message):
    sides = 6
    if args:
        try:
            sides = int(args[0])
        except ValueError:
            return "Please specify an integer!"

    if sides > 0:
        random_side = random.randint(1, int(sides))
        return "Rolling {}-sided die: {}".format(sides, random_side)
    else:
        return "Please specify a positive integer!"