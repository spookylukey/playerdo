from playerdo.backends.base import Player
from playerdo.utils import process_stdout, process_retval


class Moc(Player):

    process_name = "mocp"
    friendly_name = "moc"

    def is_stopped(self):
        info = process_stdout(["mocp", "-i"])
        return "State: STOP" in info

    def is_paused(self):
        info = process_stdout(["mocp", "-i"])
        return "State: PAUSE" in info

    def play(self):
        process_retval(["mocp", "--play"])

    def pause(self):
        process_retval(["mocp", "--pause"])

    def unpause(self):
        process_retval(["mocp", "--unpause"])

    def stop(self):
        process_retval(["mocp", "--stop"])

    def next(self):
        process_retval(["mocp", "--next"])

    def prev(self):
        process_retval(["mocp", "--previous"])
