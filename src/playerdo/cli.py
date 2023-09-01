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
from playerdo.main import do_command, do_test, find_players, is_playing


def make_command_help():
    command_help = "The command to run. The following commands are available: \n\n"

    max_len = len(sorted(commands, key=lambda c: len(c[0]))[-1][0])

    for name, doc, f in commands:
        command_help += "  " + name + " " * (max_len - len(name) + 2) + doc + "\n"

    command_help += """
Not all operations are supported or fully supported by all players.
    """
    return command_help


def make_player_help(players):
    help = """
Currently supported players (in the order they will currently be used):

"""
    for p in players:
        n = getattr(p, "friendly_name", None)
        if n is not None:
            help += "  " + n + "\n"

    return help


# List of commands: (name, docstring, callable)
# The callable must accept a single argument, a list of players.
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
        def command(players):
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
    players = find_players()
    parser = argparse.ArgumentParser(
        prog=f"player_do {__version__}",
        description=(
            """Media players that are currently running will be detected,
and the command will be passed on to the first, giving
priority to players that seem to be active."""
        ),
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=make_player_help(players),
    )

    parser.add_argument("command", help=make_command_help())

    args = parser.parse_args()

    command = command_dict.get(args.command, None)
    if command is None:
        sys.stderr.write(f"Unrecognised command '{args.command}'.\n\n")
        parser.print_help()
        sys.exit(1)
    else:
        command(players)


if __name__ == "__main__":
    sys.exit(main())
