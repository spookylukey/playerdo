#!/usr/bin/env python3

#
# Wrapper for controlling various music players, so that you can define
# keyboard shortcuts that work for whatever player you are using.  Ideally it
# will still work even if multiple players are running if all but one are
# 'stopped', but some music players do not have such a state or it cannot be
# determined.
#
import argparse
import sys

from playerdo import __version__, install
from playerdo.backends.base import Player
from playerdo.main import do_command, do_test, find_player_classes, find_players_sorted, get_broken_backends, is_playing
from playerdo.utils import BackendBrokenException


def make_command_help():
    command_help = "The command to run. The following commands are available: \n\n"

    max_len = len(sorted(commands, key=lambda c: len(c[0]))[-1][0])

    for name, doc, f in commands:
        command_help += "  " + name + " " * (max_len - len(name) + 2) + doc + "\n"

    command_help += """
Not all operations are supported or fully supported by all players.
    """
    return command_help


def make_player_help(player_classes, sorted_players):
    help = """
Active players (in the order they will currently be used):

"""
    seen_classes = set()
    for player in sorted_players:
        try:
            running = player.is_running()
        except (NotImplementedError, BackendBrokenException):
            running = False
        if running:
            help += f"  {player.friendly_name}\n"
            seen_classes.add(player.__class__)

    unseen_classes = set(player_classes) - seen_classes
    broken_classes = get_broken_backends(unseen_classes)
    unused_classes = set(cls for cls in unseen_classes if cls not in broken_classes)

    if unused_classes:
        help += "\nInactive backends/players:\n\n"
        for cls in sorted(unused_classes, key=lambda cls: cls.friendly_name):
            help += f"  {cls.friendly_name}\n"

    if broken_classes:
        help += "\nUnusable backends:\n\n"
        for cls, errors in broken_classes.items():
            help += f"  {cls.friendly_name}:\n"
            for error in errors:
                help += f"    - {error}\n"

    return help


# List of commands: (name, docstring, callable)
# The callable must accept two arguments, a list of player classes and a list of player instances
commands = []

for c in [
    "play",
    "pause",
    "unpause",
    "togglepause",
    "playpause",
    "stop",
    "next",
    "prev",
    "osd",
]:

    def mk_command(name):
        def command(player_classes, players):
            return do_command(name, players)

        return command

    commands.append((c, getattr(Player, c).__doc__.strip().replace("\n", " "), mk_command(c)))

commands.extend(
    [
        (
            "is_playing",
            "Exits status 0 if a player is playing, otherwise 1",
            is_playing,
        ),
        ("test", "Tests that all dependencies are available.", do_test),
        (
            "install_gnome",
            "Install keybindings for GNOME2 and launch keybinding editor",
            lambda *args: install.install_gnome(),
        ),
        (
            "install_mate",
            "Install keybindings for Mate and launch keybinding editor",
            lambda *args: install.install_mate(),
        ),
        (
            "install_gnome3",
            "Install keybindings for GNOME3 and launch keybinding editor",
            lambda *args: install.install_gnome3(),
        ),
        (
            "install_cinnamon",
            "Install keybindings for Cinnamon and launch keybinding editor",
            lambda *args: install.install_cinnamon(),
        ),
    ]
)

command_dict = dict((name, f) for name, doc, f in commands)


def main():
    player_classes = find_player_classes()
    players = find_players_sorted()
    parser = argparse.ArgumentParser(
        prog="player_do",
        description=(
            """Media players that are currently running will be detected,
and the command will be passed on to the first, giving
priority to players that seem to be active."""
        ),
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=make_player_help(player_classes, players),
    )

    parser.add_argument(
        "-p", "--player", help="Send commands to the given player (with name chosen from the list below)"
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("command", help=make_command_help())

    args = parser.parse_args()

    command = command_dict.get(args.command, None)
    if command is None:
        sys.stderr.write(f"Unrecognised command '{args.command}'.\n\n")
        parser.print_help()
        sys.exit(1)
    else:
        if args.player:
            chosen_players = [player for player in players if player.friendly_name == args.player]
            if not chosen_players:
                sys.stderr.write(f"Player '{args.player}' not recognised\n")
                sys.exit(1)
        else:
            chosen_players = players
        command(player_classes, chosen_players)


if __name__ == "__main__":
    sys.exit(main())
