import random

# This field will contain an OmniInterface object when init() is called
omni = None

"""
init is used to initialize the commands specified in this module, using the
interface that was placed in the omni variable before init() is called
"""
def init():
    omni.add_command(marco_polo, 'marco', "He'll be fine")
    omni.add_command(roll, 'roll', 'Rolls a 6-sided die, or an n-sided die if an integer n is provided')
    omni.add_command(eight_ball, '8ball', "Answers your pressing yes/no questions ending in a question mark, such as:\nShould I eat cereal in the shower?\nAre you sentient?\nPizza?")
    omni.add_command(draw_card, 'drawCard', 'Draws a random card from a standard playing deck')
    omni.add_command(flip_coin, 'flipCoin', 'Flips a coin')
    omni.add_command(lotto, 'lotto', 'Randomly returns one of the arguments provided')
    omni.add_command(shuffle, 'shuffle', 'Randomly shuffles the provided arguments')

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

"""
Magic 8-ball that definitively answers important questions
Includes mention of the person evoking the command in case many questions are
being asked by different people.
"""
async def eight_ball(args, message):
    if not args or not args[-1].endswith('?'):
        return "Please give me a yes or no question."

    responses = [
        "Absolutely.",
        "It is certain.",
        "Without a doubt.",
        "Yes, definitely.",
        "You may rely on it.",
        "Most likely.",
        "Yes.",
        "Ask again later.",
        "I can't tell.",
        "I better not tell you now.",
        "I'm not sure.",
        "I don't know.",
        "Don't count on it.",
        "No.",
        "Very doubtful.",
        "Not really.",
        "Outlook isn't great.",
        "Not at all.",
        "My sources say no.",
        "Nope!"
        ]
    return '<@{}> {}'.format(message.author.id, random.choice(responses))

"""
Draws a random card from a standard playing deck
"""
async def draw_card(args, message):

    value_list = list(range(2,11)) + ['jack', 'queen', 'king', 'ace']
    suit_list = ['hearts', 'diamonds', 'spades', 'clubs']

    value = random.choice(value_list)
    suit = random.choice(suit_list)

    return "Your card is the {} of {}".format(value, suit)


"""
Flips a coin
"""
async def flip_coin(args, message):
    return "It's {}!".format(random.choice(['heads','tails']))

"""
Takes any number of arguments and return one of them randomly.
"""
async def lotto(args, message):
    if not args:
        response = "I can't choose anything if you don't give me any options!"
    else:
        options = message.content.split()[1:]
        response = random.choice(options)
    return response

"""
Randomly shuffles the arguments and returns them
"""
async def shuffle(args, message):
    random.shuffle(args)
    return ', '.join(args)
