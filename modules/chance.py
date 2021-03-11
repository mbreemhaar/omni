import random
from omni_utils import OmniInterface
omni = OmniInterface()


@omni.command('roll', 'Rolls a 6-sided die, or an n-sided die if an integer n is provided')
def roll(args):
    """
    Command to roll a die
    """

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

@ omni.command('8ball',
"""Answers your pressing yes/no questions ending in a question mark, such as:\n"
Should I eat cereal in the shower?\nAre you sentient?\nPizza?""")
def eight_ball(args, message):
    """
    Magic 8-ball that definitively answers important questions
    Includes mention of the person evoking the command in case many questions are
    being asked by different people.
    """

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

@omni.command('drawCard', 'Draws a random card from a standard playing deck')
def draw_card():
    """
    Draws a random card from a standard playing deck
    """

    value_list = list(range(2,11)) + ['jack', 'queen', 'king', 'ace']
    suit_list = ['hearts', 'diamonds', 'spades', 'clubs']

    value = random.choice(value_list)
    suit = random.choice(suit_list)

    return "Your card is the {} of {}".format(value, suit)


@omni.command('flipCoin', 'Flips a coin')
def flip_coin():
    """
    Flips a coin
    """

    return "It's {}!".format(random.choice(['heads','tails']))


@omni.command('lotto', 'Randomly returns one of the arguments provided')
def lotto(args):
    """
    Takes any number of arguments and return one of them randomly.
    """

    if not args:
        return "I can't choose anything if you don't give me any options!"
    else:
        return random.choice(args)


@omni.command('shuffle', 'Randomly shuffles the provided arguments')
def shuffle(args):
    """
    Randomly shuffles the arguments and returns them
    """

    random.shuffle(args)
    return ', '.join(args)
