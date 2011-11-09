from playerdo.backends.base import Player
from playerdo.utils import process_retval, process_stdout, program_running


class Banshee(Player):

    process_name = "banshee-1"
    friendly_name = "Banshee"

    def is_running(self):
        return program_running("banshee-1") or program_running("banshee")

    def is_stopped(self):
        return process_stdout(["banshee", "--query-current-state"]).strip() \
            ==  "current-state: idle"

    def is_paused(self):
        return process_stdout(["banshee", "--query-current-state"]).strip() \
            ==  "current-state: paused"

    def play(self):
        process_retval(["banshee", "--play"])

    def pause(self):
        process_retval(["banshee", "--pause"])

    def unpause(self):
        self.play()

    def togglepause(self):
        process_retval(["banshee", "--toggle-playing"])

    def stop(self):
        process_retval(["banshee", "--stop"])

    def next(self):
        process_retval(["banshee", "--next"])

    def prev(self):
        process_retval(["banshee", "--restart-or-previous"])
