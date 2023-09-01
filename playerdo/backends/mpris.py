from playerdo.backends.base import Player
from playerdo.utils import DBusObject

# Note that dbus is not imported at module level, to allow the
# check_dependencies functionality to be able to report the missing dbus
# dependency rather than get an ImportError


def get_all_mpris_buses():
    import dbus

    bus = dbus.SessionBus()
    return [
        str(s)
        for s in bus.list_names()
        if str(s).startswith("org.mpris.") and not str(s).startswith("org.mpris.MediaPlayer2")
    ]


def get_sorted_candidate_buses():
    import dbus

    candidates = get_all_mpris_buses()
    # Sort by status - playing = 0, paused = 1, stopped = 2
    buses = []
    for n in candidates:
        try:
            status = (int(DBusObject(n, PLAYER_OBJECT_NAME).GetStatus()[0]), n)
        except dbus.exceptions.DBusException:
            # probably 'unknown method', so we assume 'stopped'
            status = (2, n)
        buses.append(status)
    buses.sort()
    return [n for i, n in buses]


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
            buses = get_sorted_candidate_buses()
            names = []
            for n in buses:
                try:
                    bus = DBusObject(n, "/")
                    names.append(bus.Identity())
                except dbus.exceptions.DBusException:
                    bus = DBusObject(n, "/", interface=MPRIS_INTERFACE_NAME)
                    names.append(bus.Identity())

            if len(names) > 0:
                retval += f" (currently running: {', '.join(names)})"
        except Exception:
            pass

        return retval

    @property
    def bus_name(self):
        try:
            return self._bus_name
        except AttributeError:
            buses = get_sorted_candidate_buses()
            if len(buses) > 0:
                bus_name = buses[0]
            else:
                bus_name = None
            self._bus_name = bus_name
            return bus_name

    @property
    def dbus_obj(self):
        bus_name = self.bus_name

        if bus_name is None:
            raise NotImplementedError

        try:
            return self._dbus_obj
        except AttributeError:
            return self._init_dbus()

    def _init_dbus(self):
        if not hasattr(self, "_dbus_obj"):
            player = DBusObject(self.bus_name, PLAYER_OBJECT_NAME, interface=MPRIS_INTERFACE_NAME)
            self._dbus_obj = player
        return self._dbus_obj

    def is_running(self):
        try:
            import dbus
        except ImportError:
            return False

        if self.bus_name is None:
            return False
        try:
            self._init_dbus()
            return True
        except dbus.DBusException:
            return False

    def is_paused(self):
        import dbus

        try:
            return self.dbus_obj.GetStatus()[0] == 1
        except dbus.exceptions.DBusException:
            # Assume stopped, not paused, if doesn't support GetStatus
            return False

    def is_stopped(self):
        import dbus

        try:
            return self.dbus_obj.GetStatus()[0] == 2
        except dbus.exceptions.DBusException:
            # Assume stopped if doesn't support GetStatus
            return True

    def is_playing(self):
        import dbus

        try:
            return self.dbus_obj.GetStatus()[0] == 0
        except dbus.exceptions.DBusException:
            # Assume stopped, not playing, if doesn't support GetStatus
            return False

    def check_dependencies(self):
        retval = []
        try:
            import dbus  # noqa
        except ImportError:
            retval.append("dbus Python bindings are required")
        return retval

    def play(self):
        self.dbus_obj.Play()

    def pause(self):
        self.dbus_obj.Pause()

    def unpause(self):
        self.play()

    def playpause(self):
        import dbus

        try:
            # Some define this e.g. Exaile
            self.dbus_obj.PlayPause()
        except dbus.DBusException:
            super().playpause()

    def next(self):
        self.dbus_obj.Next()

    def prev(self):
        self.dbus_obj.Prev()

    def stop(self):
        self.dbus_obj.Stop()

    def osd(self):
        self.dbus_obj.ShowOSD()
