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


class Mpris2Player(Player):
    _friendly_name = "MPRIS2"
    friendly_name = "MPRRIS2"

    # We put this lower than default, because MPRIS covers a lot of players,
    # including web browsers. If someone has another Music app running, it's
    # likely that's what they want player_do to control.
    sort_order = 5

    @classmethod
    def get_instances(cls):
        if cls.check_dependencies():
            return []
        return [cls._make_instance(bus) for bus in get_all_mpris_buses()]

    @classmethod
    def _make_instance(cls, bus_name: str):
        props = DBusProperties(bus_name, PLAYER_OBJECT_NAME, MAIN_INTERFACE_NAME)
        app_identity = props.get("Identity")
        return cls(name=f"{cls.friendly_name}:{app_identity}", bus_name=bus_name)

    def __init__(self, *, name, bus_name):
        self.friendly_name = name
        self.bus_name = bus_name
        self.dbus_obj = DBusObject(bus_name, PLAYER_OBJECT_NAME, PLAYER_INTERFACE_NAME)

    def _playback_status(self):
        props = DBusProperties(self.bus_name, PLAYER_OBJECT_NAME, PLAYER_INTERFACE_NAME)
        return str(props.get("PlaybackStatus"))

    def is_running(self):
        # The instance only exists if the player is running
        return True

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
