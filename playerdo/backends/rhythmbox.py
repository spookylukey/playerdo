from playerdo.backends.base import Player
from playerdo.utils import process_retval


class RhythmBox(Player):

    process_name = "rhythmbox"
    friendly_name = "rhythmbox"

    def is_stopped(self):
        # rhythmbox doesn't seem to have this state
        return False

    # is_paused - no way to know

    def play(self):
        process_retval(["rhythmbox-client", "--play"])

    def pause(self):
        process_retval(["rhythmbox-client", "--pause"])

    def unpause(self):
        self.play()

    def togglepause(self):
        process_retval(["rhythmbox-client", "--play-pause"])

    def stop(self):
        # This isn't quite right, but better than nothing
        self.pause()

    def next(self):
        process_retval(["rhythmbox-client", "--next"])

    def prev(self):
        process_retval(["rhythmbox-client", "--previous"])
