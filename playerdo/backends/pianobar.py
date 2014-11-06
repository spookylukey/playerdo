import os
import os.path

from playerdo.backends.base import Player

class PianoBar(Player):

    process_name = "pianobar"
    friendly_name = "pianobar"

    def __init__(self):
        self._fifo = os.path.join(os.environ['HOME'], '.config', 'pianobar', 'ctl')

    def _send(self, cmd):
        if os.path.exists(self._fifo):
            with open(self._fifo, 'wb') as f:
                f.write(cmd.encode('ascii'))

    def check_dependencies(self):
        if not os.path.exists(self._fifo):
            return ["Could not find pianobar control fifo at '{}'".format(self._fifo)]
        return []

    def is_stopped(self):
        # Play starts as soon as it's launched, and there's no stop command
        return False

    # is_paused - no way to know
    # is_playing - no way to know

    def play(self):
        self.unpause()

    def pause(self):
        self._send('S')

    def togglepause(self):
        self._send('p')

    def unpause(self):
        self._send('P')

    def stop(self):
        self.pause()

    def next(self):
        self._send('n')

    # prev - not possible

