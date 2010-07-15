from playerdo.backends import *
from playerdo.backends.base import Player
import sys

def get_running_players(players):
    """
    Given a list of Player classes, returns a list of players (instances) that
    are running, sorted by priority they should be tried.
    """

    # Get running players
    running_ps = []
    for P in players:
        p = P()
        try:
            running = p.is_running()
            if running:
                running_ps.append(p)
        except NotImplementedError:
            pass


    # Try to find out which one is playing
    state = []
    for p in running_ps:
        try:
            is_stopped = p.is_stopped()
        except NotImplementedError:
            is_stopped = None

        if is_stopped == True:
            state.append(2)
        elif is_stopped == False:
            state.append(0)
        else:
            # In-between value for unknowns, because a player that is definitely
            # stopped is less preferred than one that *might* be playing.
            state.append(1)

    l = zip(state, running_ps)
    l.sort()

    return [x[1] for x in l]

def do_test(players):
    # Check dependencies of all players
    pass


def do_command(command, players):
    """
    Execute the given command, given a list of Player classes
    """
    candidates = get_running_players(players)
    if len(candidates) == 0:
        sys.stderr.write("No players running!\n")
        sys.exit(1)

    # Use the first one
    player = candidates[0]
    try:
        player.do_command(command)
    except NotImplementedError:
        sys.stderr.write("Operation '%s' not supported for player '%s'.\n" % (command, player.friendly_name))
        sys.exit(1)


def find_players():
    return [v for v in globals().values() if type(v) is type and issubclass(v, Player)]
