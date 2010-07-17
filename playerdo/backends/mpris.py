from playerdo.backends.base import Player
from playerdo.utils import DBusObject
import dbus


def get_all_mpris_buses():
    bus = dbus.SessionBus()
    return [str(s) for s in bus.list_names()
            if str(s).startswith('org.mpris.')]


class MprisPlayer(Player):

    friendly_name = "Any MPRIS player"
    player_object_name = "/Player"
    tracklist_object_name = "/TrackList"

    @property
    def bus_name(self):
        # Use the first one we find.
        try:
            return self._bus_name
        except AttributeError:
            candidates = get_all_mpris_buses()
            # Sort by status - playing = 0, paused = 1, stopped = 2
            l = [(int(DBusObject(n, self.player_object_name).GetStatus()[0]), n)
                 for n in candidates]
            l.sort()
            if len(l) > 0:
                bus_name = l[0][1]
            else:
                bus_name = None
            self._bus_name = bus_name
            return bus_name

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
        if self.bus_name is None:
            return False
        try:
            # Force evaluation:
            bus = self.player._bus
            return True
        except dbus.DBusException:
            return False

    def is_stopped(self):
        return self.player.GetStatus()[0] == 2

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
