import os
import os.path

from playerdo.backends.base import Player
from playerdo.backends.socket import TcpSocketPlayerMixin
from playerdo.utils import program_running


class Mpd(TcpSocketPlayerMixin, Player):

    friendly_name = "mpd"
    process_name = "mpd"

    def connect_socket(self, socket):
        retval = super(Mpd, self).connect_socket(socket)
        socket.recv(1000)  # Receive first response
        return retval

    def is_running(self):
        host, port = self.socket_address()
        if host == 'localhost':
            # We can do a check for `mpd` on this machine,
            # so we don't have to attempt a TCP connection,
            # which could hang.
            return program_running(self.process_name)
        try:
            return self.send_socket_command('status')
        except ConnectionRefusedError:
            return False

    def socket_address(self):
        # We allow configuration using same environment variables that mpc uses
        # http://manpages.ubuntu.com/manpages/trusty/man1/mpc.1.html
        host = os.environ.get('MPD_HOST', 'localhost')
        port = os.environ.get('MPD_PORT', 6600)
        return (host, port)

    def is_stopped(self):
        return 'state: stop' in self.send_socket_command('status').split("\n")

    def is_paused(self):
        return 'status: pause' in self.send_socket_command('status').split("\n")

    def is_playing(self):
        return 'status: play' in self.send_socket_command('status').split("\n")

    def play(self):
        self.send_socket_command('play')

    def pause(self):
        self.send_socket_command("pause")

    def unpause(self):
        self.play()

    def stop(self):
        self.send_socket_command("stop")

    def next(self):
        self.send_socket_command("next")

    def prev(self):
        self.send_socket_command("previous")
