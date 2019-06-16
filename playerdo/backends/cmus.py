import os
import os.path

from playerdo.backends.base import Player
from playerdo.backends.socket import UnixSocketPlayerMixin
from playerdo.utils import process_retval, BackendBrokenException

class Cmus(UnixSocketPlayerMixin, Player):

    process_name = "cmus"
    friendly_name = "cmus"

    def socket_path(self):
        for f in [
                os.path.join(os.environ['XDG_RUNTIME_DIR'], 'cmus-socket'),
                os.path.join(os.environ['HOME'], '.cmus', 'socket'),
        ]:
            if os.path.exists(f):
                return f
        raise BackendBrokenException("cmus is running, but its socket is not found")

    def is_stopped(self):
        return 'status stopped' in self.send_socket_command('status')

    def is_paused(self):
        return 'status paused' in self.send_socket_command('status')

    def is_playing(self):
        return 'status playing' in self.send_socket_command('status')

    def play(self):
        self.send_socket_command('player-play')

    def pause(self):
        self.send_socket_command("player-pause")

    def unpause(self):
        self.pause()

    def stop(self):
        self.send_socket_command("player-stop")

    def next(self):
        self.send_socket_command("player-next")

    def prev(self):
        self.send_socket_command("player-prev")
