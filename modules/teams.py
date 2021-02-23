import random
from itertools import cycle

omni = None


def init():
    omni.add_command(teams, 'teams', 'Creates n evenly divided teams with the names provided')


async def teams(args, message):

    # Take the number of teams and player names from the given arguments
    try:
        n_teams = int(args[0])
        players = args[1:]
    except (ValueError, IndexError):
        return 'Give me the number of teams you want, followed by the list of player names'

    # If there are more teams than players, that number of teams is impossible to make
    n_players = len(players)
    if n_teams > n_players:
        return f'I can\'t make {n_teams} teams with only {n_players} players...'

    # Randomize the order of the list of players
    random.shuffle(players)

    # Initialize a list to store all teams and set up an iterator to loop over teams in a cycle
    teams_list = [[] for _ in range(n_teams)]
    teams_iter = cycle(teams_list)

    # Loop over players and add each one to a team
    for p in players:
        next(teams_iter).append(p)

    # Shuffle the order of the teams so the last won't always be the smallest team
    random.shuffle(teams_list)

    # Generate a response listing the teams to send to the user
    response = ''
    for idx, t in enumerate(teams_list):
        response += f'Team {idx + 1}: ' + ', '.join(t) + '\n'

    return response
