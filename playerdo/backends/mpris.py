from playerdo.backends.base import Player
from playerdo.utils import DBusObject
import dbus


class MprisPlayer(Player):

    bus_name = None
    player_object_name = "/Player"
    tracklist_object_name = "/TrackList"

    @property
    def player(self):
        if self.bus_name is None or self.player_object_name is None:
            raise NotImplementedError

        try:
            return self._player
        except AttributeError:
            obj = DBusObject(self.bus_name, self.player_object_name)
            self._player = obj
            return obj

    @property
    def tracklist(self):
        if self.bus_name is None or self.tracklist_object_name is None:
            raise NotImplementedError

        try:
            return self._tracklist
        except AttributeError:
            obj = DBusObject(self.bus_name, self.tracklist_object_name)
            self._tracklist = obj
            return obj

    def is_running(self):
        # pidof doesn't work for some apps (e.g. exaile), but this should work
        # for all Mpris apps.
        try:
            # Force evaluation:
            bus = self.player._bus
            return True
        except dbus.DBusException:
            return False

    def is_stopped(self):
        # This seems to work for exaile and clementine
        return self.tracklist.GetCurrentTrack() == -1

    def play(self):
        self.player.Play()

    def pause(self):
        self.player.Pause()

    def unpause(self):
        self.play()

    def playpause(self):
        try:
            # Some define this e.g. Exaile
            self.player.PlayPause()
        except dbus.DBusException:
            super(MprisPlayer, self).playpause()

    def next(self):
        self.player.Next()

    def prev(self):
        self.player.Prev()

    def stop(self):
        self.player.Stop()

    def osd(self):
        self.player.ShowOSD()


