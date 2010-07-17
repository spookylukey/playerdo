from playerdo.backends.base import Player
from playerdo.utils import process_retval, PlayerException
import os


class ShellFm(Player):
    # Requirements:
    #  shc (compiled version of shc.hs from shell-fm's sources)

    process_name = "shell-fm"
    friendly_name = "shell-fm"

    def is_stopped(self):
        return not os.path.isfile(os.path.join(os.environ['HOME'],
                                               ".shell-fm",
                                               "nowplaying"))

    def check_dependencies(self):
        if process_retval(["which", "shc"]) != 0:
            return ["The command line program 'shc', compiled from the shc.hs script that comes with shell-fm, needs to be present on your PATH."]
        return []

    def play(self):
        if not self.is_stopped():
            self.unpause()
        else:
            raise PlayerException("Cannot play shell-fm when in a stopped state.")

    def pause(self):
        process_retval(["shc", "pause"])

    def unpause(self):
        self.pause()

    def stop(self):
        process_retval(["shc", "stop"])

    def next(self):
        process_retval(["shc", "next"])
