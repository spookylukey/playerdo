from playerdo.backends.base import Player
from playerdo.utils import DBusObject


def get_all_mpris_buses():
    import dbus
    bus = dbus.SessionBus()
    return [str(s) for s in bus.list_names()
            if str(s).startswith('org.mpris.')]


def get_sorted_candidate_buses(player_object_name):
    candidates = get_all_mpris_buses()
    # Sort by status - playing = 0, paused = 1, stopped = 2
    l = [(int(DBusObject(n, player_object_name).GetStatus()[0]), n)
         for n in candidates]
    l.sort()
    return [n for i, n in l]


class MprisPlayer(Player):

    _friendly_name = "Any MPRIS player"
    player_object_name = "/Player"

    @property
    def friendly_name(self):
        retval = self._friendly_name
        try:
            l = get_sorted_candidate_buses(self.player_object_name)
            names = []
            for n in l:
                try:
                    bus = DBusObject(n, "/")
                    names.append(bus.Identity())
                except:
                    pass

            if len(names) > 0:
                retval += " (currently running: %s)" %  ", ".join(names)
        except Exception:
            pass

        return retval

    @property
    def bus_name(self):
        try:
            return self._bus_name
        except AttributeError:
            l = get_sorted_candidate_buses(self.player_object_name)
            if len(l) > 0:
                bus_name = l[0]
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

    def is_running(self):
        try:
            import dbus
        except ImportError:
            return False

        if self.bus_name is None:
            return False
        try:
            # Force evaluation:
            bus = self.player._bus
            return True
        except dbus.DBusException:
            return False

    def is_paused(self):
        return self.player.GetStatus()[0] == 1

    def is_stopped(self):
        return self.player.GetStatus()[0] == 2

    def check_dependencies(self):
        retval = []
        try:
            import dbus
        except ImportError:
            retval.append("dbus Python bindings are required")
        return retval

    def play(self):
        self.player.Play()

    def pause(self):
        self.player.Pause()

    def unpause(self):
        self.play()

    def playpause(self):
        import dbus
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
