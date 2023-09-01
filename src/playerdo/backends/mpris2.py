from playerdo.backends.base import Player
from playerdo.utils import DBusObject, DBusProperties

# Note that dbus is not imported at module level, to allow the
# check_dependencies functionality to be able to report the missing dbus
# dependency rather than get an ImportError


def get_all_mpris_buses():
    import dbus

    bus = dbus.SessionBus()
    return [str(s) for s in bus.list_names() if str(s).startswith("org.mpris.MediaPlayer2")]


playback_status_levels = {
    "Playing": 0,
    "Paused": 1,
    "Stopped": 2,
}


PLAYER_OBJECT_NAME = "/org/mpris/MediaPlayer2"
MAIN_INTERFACE_NAME = "org.mpris.MediaPlayer2"
PLAYER_INTERFACE_NAME = "org.mpris.MediaPlayer2.Player"


def get_sorted_candidate_buses():
    candidates = get_all_mpris_buses()
    # Sort by PlaybackStatus
    buses = []
    for n in candidates:
        state = str(DBusProperties(n, PLAYER_OBJECT_NAME, PLAYER_INTERFACE_NAME).get("PlaybackStatus"))
        buses.append((playback_status_levels[state], n))
    buses.sort()
    return [n for i, n in buses]


class Mpris2Player(Player):
    _friendly_name = "MPRIS2"
    friendly_name = "MPRRIS2"

    sort_order = 5

    def __init__(self):
        self.set_friendly_name()

    def set_friendly_name(self):
        name = self._friendly_name
        try:
            buses = get_sorted_candidate_buses()
            names = []

            for n in buses:
                props = DBusProperties(n, PLAYER_OBJECT_NAME, MAIN_INTERFACE_NAME)
                names.append(props.get("Identity"))

            if len(names) > 0:
                name += f" (currently running: {', '.join(names)})"
        except Exception:
            pass
        self.friendly_name = name

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
            obj = DBusObject(self.bus_name, PLAYER_OBJECT_NAME, PLAYER_INTERFACE_NAME)
            self._dbus_obj = obj
        return self._dbus_obj

    def _playback_status(self):
        props = DBusProperties(self.bus_name, PLAYER_OBJECT_NAME, PLAYER_INTERFACE_NAME)
        return str(props.get("PlaybackStatus"))

    def is_running(self):
        try:
            import dbus
        except ImportError:
            return False

        if self.bus_name is None:
            return False
        try:
            # Force evaluation:
            self._init_dbus()
            return True
        except dbus.DBusException:
            return False

    def is_paused(self):
        return self._playback_status() == "Paused"

    def is_stopped(self):
        return self._playback_status() == "Stopped"

    def is_playing(self):
        return self._playback_status() == "Playing"

    @classmethod
    def check_dependencies(cls):
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
        self.dbus_obj.PlayPause()

    def next(self):
        self.dbus_obj.Next()

    def prev(self):
        self.dbus_obj.Previous()

    def stop(self):
        self.dbus_obj.Stop()

    def osd(self):
        raise NotImplementedError()
