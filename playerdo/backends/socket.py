from __future__ import absolute_import

import socket


class SocketPlayerBase(object):
    def send_socket_command(self, command):
        s = self.get_open_socket()
        s.send((command + "\n").encode("ascii"))
        # We never know how much to receive, most of these
        # protocols send very little data back for the commands
        # we use.
        return s.recv(2048)

    def get_open_socket(self):
        if hasattr(self, '_socket'):
            return self._socket
        s = self.create_socket()
        self.connect_socket(s)
        self._socket = s
        # We'll leave it to Python to clean this up when
        # the script exits...
        return s

    def create_socket(self):
        raise NotImplentedError()

    def connect_socket(self, socket):
        raise NotImplentedError()


class TcpSocketPlayerMixin(SocketPlayerBase):

    def create_socket(self):
        return socket.socket()

    def connect_socket(self, socket):
        socket.connect(self.socket_address())

    def socket_address(self):
        raise NotImplementedError()


class UnixSocketPlayerMixin(SocketPlayerBase):

    def create_socket(self):
        return socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def connect_socket(self, socket):
        socket.connect(self.socket_path())

    def socket_path(self):
        raise NotImplentedError()
