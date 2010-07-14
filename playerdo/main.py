#!/usr/bin/env python

#
# Wrapper for controlling various music players, so that you can define keyboard
# shortcuts that work for whatever player you are using.  Ideally it will still
# work even if multiple players are running if all but one are 'stopped', but
# some music players do not have such a state or it cannot be determined.
#

import sys

# Execute commands:

def main(command, players):
    if command == "test":
        do_test(players)
    elif command == "help":
        print_help(players)
    else:
        do_command(command, players)


def do_test(players):
    # Check dependencies of all players
    pass


def print_help(players):
    # Print help and list of supported players
    pass

def do_command(command, players):
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

    if len(running_ps) == 0:
        sys.stderr.write("No players running!\n")
        sys.exit(1)


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

    # Use the first one
    player = l[0][1]
    try:
        player.do_command(command)
    except NotImplementedError:
        sys.stderr.write("Operation '%s' not support for player '%s'." % (command, player.__name__))
        sys.exit(1)

from playerdo.backends import *
from playerdo.backends.base import Player

def find_players():
    return [v for v in globals().values() if type(v) is type and issubclass(v, Player)]

if __name__ == '__main__':
    import sys
    main(sys.argv[1], find_players())

