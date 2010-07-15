from playerdo.backends.base import Player
from playerdo.utils import process_retval
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

    # Can't implement 'play', because once you are stopped, shell-fm/shc needs
    # you to specify a station if you want it to play.

    def pause(self):
        process_retval(["shc", "pause"])

    def unpause(self):
        self.pause()

    def stop(self):
        process_retval(["shc", "stop"])

    def next(self):
        process_retval(["shc", "next"])
