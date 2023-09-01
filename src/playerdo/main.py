from __future__ import annotations

import sys

from playerdo.backends.base import Player
from playerdo.utils import BackendBrokenException, PlayerException


def sort_players(players):
    """
    Returns list of players, sorted by priority.
    """

    def key(player):
        running = False
        try:
            running = player.is_running()
        except (NotImplementedError, BackendBrokenException):
            running = False

        if not running:
            state = 3
        else:
            try:
                is_stopped = player.is_stopped()
            except (NotImplementedError, BackendBrokenException):
                is_stopped = None

            if is_stopped is True:
                state = 2
            elif is_stopped is False:
                state = 0
            else:
                # In-between value for unknowns, because a player that is
                # definitely stopped is less preferred than one that *might* be
                # playing.
                state = 1
        return (state, player.sort_order, player.friendly_name)

    return sorted(players, key=key)


def do_test(player_classes, players):
    """
    Checks that all backends have required dependencies, printing any failures
    """
    for cls, errors in get_broken_backends(player_classes).items():
        sys.stdout.write(f"Player '{cls.friendly_name}' has missing dependencies:\n")
        for error in errors:
            sys.stdout.write(f" - {error}\n")


def do_command(command, players):
    """
    Execute the given command, given a list of Player classes
    """
    for player in players:
        try:
            if not player.is_running():
                continue
        except NotImplementedError:
            continue

        # Use the first one
        try:
            return player.do_command(command)
        except NotImplementedError:
            sys.stderr.write(f"Operation '{command}' not supported for player '{player.friendly_name}'.\n")
            sys.exit(1)
        except PlayerException as e:
            sys.stderr.write(e.message + "\n")
            sys.exit(1)
    sys.stderr.write("No players running!\n")
    sys.exit(1)


def is_playing(player_classes, players):
    retval = do_command("is_playing", players)
    if retval:
        sys.exit(0)
    else:
        sys.exit(1)


def find_players_sorted():
    return sort_players([instance for cls in find_player_classes() for instance in cls.get_instances()])


def find_player_classes():
    import playerdo.backends  # noqa:F401

    return [cls for cls in get_subclasses(Player) if getattr(cls, "friendly_name", None) is not None]


def get_subclasses(cls):
    subclasses = cls.__subclasses__()
    for subclass in subclasses:
        subclasses.extend(get_subclasses(subclass))
    return subclasses


def get_broken_backends(player_classes) -> dict[type, list[str]]:
    broken_classes = {}
    for cls in player_classes:
        errors = cls.check_dependencies()
        if errors:
            broken_classes[cls] = errors
    return broken_classes
