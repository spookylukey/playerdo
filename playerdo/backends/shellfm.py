import os.path
import re
import socket

from playerdo.backends.base import Player
from playerdo.utils import process_retval, PlayerException

class ShellFm(Player):

    process_name = "shell-fm"
    friendly_name = "shell-fm"

    def _socket_path(self):
        rc_path = os.path.join(os.environ['HOME'], '.shell-fm', 'shell-fm.rc')
        conf = open(rc_path).read()
        return re.search(r'^\s*unix\s*=\s*([^#\s]+)', conf, re.MULTILINE).groups()[0]

    def _send_command(self, command):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self._socket_path())
        s.send((command + "\n").encode("ascii"))
        s.close()

    def is_stopped(self):
        return not os.path.isfile(os.path.join(os.environ['HOME'],
                                               ".shell-fm",
                                               "nowplaying"))

    def check_dependencies(self):
        retval = []
        try:
            p = self._socket_path()
        except Exception:
            retval.append("Cannot find configuration file ~/.shell-fm/shell-fm.rc, or the 'unix' configuration item in that file.")
        return retval

    def play(self):
        if not self.is_stopped():
            self.unpause()
        else:
            raise PlayerException("Cannot play shell-fm when in a stopped state.")

    def pause(self):
        self._send_command("pause")

    def unpause(self):
        self.pause()

    def stop(self):
        self._send_command("stop")

    def next(self):
        self._send_command("skip")
