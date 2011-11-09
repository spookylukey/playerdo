from playerdo.backends.base import Player
from playerdo.utils import process_stdout, process_retval


class Quodlibet(Player):

    friendly_name = "quodlibet"

    def is_running(self):
        processes = process_stdout(["ps", "-A", "-o", "cmd"]).decode('ascii').split("\n")
        return len([p for p in processes
                if (p.startswith("python")
                    and ("quodlibet" in p))]) > 0

    def is_paused(self):
        return process_stdout(["quodlibet", "--status"]).decode('ascii').strip().split(' ')[0:1] == ["paused"]

    def is_stopped(self):
        # Has no concept of 'stopped'
        return self.is_paused()

    def play(self):
        process_retval(["quodlibet", "--play"])

    def pause(self):
        process_retval(["quodlibet", "--pause"])

    def unpause(self):
        self.play()

    def playpause(self):
        process_retval(["quodlibet", "--play-pause"])

    def togglepause(self):
        self.playpause()

    def next(self):
        process_retval(["quodlibet", "--next"])

    def prev(self):
        process_retval(["quodlibet", "--previous"])

    def stop(self):
        self.pause()
