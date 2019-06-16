import os.path
import re

from playerdo.backends.base import Player
from playerdo.backends.socket import UnixSocketPlayerMixin
from playerdo.utils import process_retval, PlayerException

class ShellFm(UnixSocketPlayerMixin, Player):

    process_name = "shell-fm"
    friendly_name = "shell-fm"

    def socket_path(self):
        rc_path = os.path.join(os.environ['HOME'], '.shell-fm', 'shell-fm.rc')
        conf = open(rc_path).read()
        return re.search(r'^\s*unix\s*=\s*([^#\s]+)', conf, re.MULTILINE).groups()[0]

    def _get_status(self):
        # This only works with shell-fm 0.8 and greater
        return self.send_socket_command("status").strip()

    def is_stopped(self):
        return self._get_status() == "STOPPED"

    def is_paused(self):
        return self._get_status() == "PAUSED"

    def is_playing(self):
        return self._get_status() == "PLAYING"

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
        if not self.is_paused():
            self.send_socket_command("pause")

    def unpause(self):
        if self.is_paused():
            self.send_socket_command("pause")

    def stop(self):
        self.send_socket_command("stop")

    def next(self):
        self.send_socket_command("skip")
