from playerdo.backends.base import Player
from playerdo.utils import DBusObject


def get_all_mpris_buses():
    import dbus
    bus = dbus.SessionBus()
    return [str(s) for s in bus.list_names()
            if str(s).startswith('org.mpris.')
            and not str(s).startswith('org.mpris.MediaPlayer2')]

def get_sorted_candidate_buses():
    import dbus
    candidates = get_all_mpris_buses()
    # Sort by status - playing = 0, paused = 1, stopped = 2
    l = []
    for n in candidates:
        try:
            status = (int(DBusObject(n, PLAYER_OBJECT_NAME).GetStatus()[0]), n)
        except dbus.exceptions.DBusException:
            # probably 'unknown method', so we assume 'stopped'
            status = (2, n)
        l.append(status)
    l.sort()
    return [n for i, n in l]


PLAYER_OBJECT_NAME = "/Player"
MPRIS_INTERFACE_NAME = "org.freedesktop.MediaPlayer"

class MprisPlayer(Player):

    _friendly_name = "Any MPRIS 1 player"

    # This is a generic interface, so it less preferred

    sort_order = 10

    @property
    def friendly_name(self):
        try:
            import dbus
        except ImportError:
            return self._friendly_name

        retval = self._friendly_name
        try:
            l = get_sorted_candidate_buses()
            names = []
            for n in l:
                try:
                    bus = DBusObject(n, "/")
                    names.append(bus.Identity())
                except dbus.exceptions.DBusException:
                    bus = DBusObject(n, "/", interface=MPRIS_INTERFACE_NAME)
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
            l = get_sorted_candidate_buses()
            if len(l) > 0:
                bus_name = l[0]
            else:
                bus_name = None
            self._bus_name = bus_name
            return bus_name

    @property
    def player(self):
        bus_name = self.bus_name

        if bus_name is None:
            raise NotImplementedError

        try:
            return self._player
        except AttributeError:
            obj = DBusObject(self.bus_name, PLAYER_OBJECT_NAME, interface=MPRIS_INTERFACE_NAME)
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
        import dbus
        try:
            return self.player.GetStatus()[0] == 1
        except dbus.exceptions.DBusException:
            # Assume stopped, not paused, if doesn't support GetStatus
            return False

    def is_stopped(self):
        import dbus
        try:
            return self.player.GetStatus()[0] == 2
        except dbus.exceptions.DBusException:
            # Assume stopped if doesn't support GetStatus
            return True

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
