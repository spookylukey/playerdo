import os.path
import re

from playerdo.backends.base import Player
from playerdo.backends.socket import SocketPlayerMixin
from playerdo.utils import process_retval, PlayerException

class ShellFm(SocketPlayerMixin, Player):

    process_name = "shell-fm"
    friendly_name = "shell-fm"

    def socket_path(self):
        rc_path = os.path.join(os.environ['HOME'], '.shell-fm', 'shell-fm.rc')
        conf = open(rc_path).read()
        return re.search(r'^\s*unix\s*=\s*([^#\s]+)', conf, re.MULTILINE).groups()[0]

    def is_stopped(self):
        return not os.path.isfile(os.path.join(os.environ['HOME'],
                                               ".shell-fm",
                                               "nowplaying"))

    def check_dependencies(self):
        retval = []
        try:
            p = self.socket_path()
        except Exception:
            retval.append("Cannot find configuration file ~/.shell-fm/shell-fm.rc, or the 'unix' configuration item in that file.")
        return retval

    def play(self):
        if not self.is_stopped():
            self.unpause()
        else:
            raise PlayerException("Cannot play shell-fm when in a stopped state.")

    def pause(self):
        self.send_socket_command("pause")

    def unpause(self):
        self.pause()

    def stop(self):
        self.send_socket_command("stop")

    def next(self):
        self.send_socket_command("skip")
