from playerdo.backends.base import Player
from playerdo.utils import process_stdout, process_retval


# Convoluted expressions fpr Python 2/3 compat
STATE_STOP = "State: STOP".encode('ascii')
STATE_PAUSE = "State: PAUSE".encode('ascii')


class Moc(Player):

    process_name = "mocp"
    friendly_name = "moc"

    def is_stopped(self):
        info = process_stdout(["mocp", "-i"])
        return STATE_STOP in info

    def is_paused(self):
        info = process_stdout(["mocp", "-i"])
        return STATE_PAUSE in info

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
