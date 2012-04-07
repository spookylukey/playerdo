import os
import os.path

from playerdo.backends.base import Player
from playerdo.backends.socket import SocketPlayerMixin
from playerdo.utils import process_retval, PlayerException

class Cmus(SocketPlayerMixin, Player):

    process_name = "cmus"
    friendly_name = "cmus"

    def socket_path(self):
        return os.path.join(os.environ['HOME'], '.cmus', 'socket')

    def is_stopped(self):
        return 'status stopped' in self.send_socket_command('status', receive=10000)

    def is_paused(self):
        return 'status paused' in self.send_socket_command('status', receive=10000)

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
