from __future__ import absolute_import

import socket

class SocketPlayerMixin(object):

    def send_socket_command(self, command, receive=0):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.socket_path())
        s.send((command + "\n").encode("ascii"))
        if receive > 0:
            retval = s.recv(receive)
        else:
            retval = None
        s.close()
        return retval

    def socket_path(self):
        raise NotImplentedError()
