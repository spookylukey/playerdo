from playerdo.backends import *
from playerdo.backends.base import Player
from playerdo.utils import PlayerException
import sys


def sort_players(players):
    """
    Returns list of players, sorted by priority.
    """
    # Try to find out which one is playing
    states = []
    orders = []
    for p in players:
        running = False
        try:
            running = p.is_running()
        except NotImplementedError:
            running = False

        if not running:
            state = 3
        else:
            try:
                is_stopped = p.is_stopped()
            except NotImplementedError:
                is_stopped = None

            if is_stopped == True:
                state = 2
            elif is_stopped == False:
                state = 0
            else:
                # In-between value for unknowns, because a player that is
                # definitely stopped is less preferred than one that *might* be
                # playing.
                state = 1

        states.append(state)
        orders.append(p.sort_order)

    l = zip(states, orders, players)
    l.sort()

    return [x[2] for x in l]

def get_running_players(players):
    """
    Given a list of Player classes, returns a list of players (instances) that
    are running.
    """
    # Get running players
    running_ps = []
    for p in players:
        try:
            running = p.is_running()
            if running:
                running_ps.append(p)
        except NotImplementedError:
            pass

    return running_ps

def do_test(players):
    """
    Checks that all backends have required dependencies, printing any failures
    """
    for p in players:
        failures = p.check_dependencies()
        if len(failures) > 0:
            sys.stdout.write("Player '%s' has missing dependencies:\n" % p.friendly_name)
            for l in failures:
                sys.stdout.write("  " + l + "\n")


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
        sys.stderr.write("Operation '%s' not supported for player '%s'.\n" %
                         (command, player.friendly_name))
        sys.exit(1)
    except PlayerException, e:
        sys.stderr.write(e.message + "\n")
        sys.exit(1)

def find_players():
    return sort_players([v() for v in globals().values()
                         if type(v) is type and issubclass(v, Player)])
