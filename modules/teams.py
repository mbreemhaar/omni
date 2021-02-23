import random
from itertools import cycle

omni = None


def init():
    omni.add_command(teams, 'teams', 'Creates n evenly divided teams with the names provided')


async def teams(args, message):
    """
    Creates n evenly divided teams with names provided.
    """

    # Take the number of teams and player names from the given arguments
    try:
        n_teams = int(args[0])
        players = args[1:]
    except (ValueError, IndexError):
        return 'Give me the number of teams you want, followed by the list of player names'

    # If the number of teams is 0 or negative...
    if n_teams <= 0:
        return f'I can\'t make {n_teams} teams'

    # If there are no players...
    n_players = len(players)
    if n_players == 0:
        return f'I can\'t make teams without any players'

    # If there are more teams than players...
    if n_teams > n_players:
        pluralize_teams = '' if n_teams == 1 else 's'
        pluralize_players = '' if n_players == 1 else 's'
        return f'I can\'t make {n_teams} team{pluralize_teams} with only {n_players} player{pluralize_players}'

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
