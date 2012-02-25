from playerdo.backends.base import Player
from playerdo.utils import DBusObject, DBusProperties


def get_all_mpris_buses():
    import dbus
    bus = dbus.SessionBus()
    return [str(s) for s in bus.list_names()
            if str(s).startswith('org.mpris.MediaPlayer2')]


playback_status_levels = {
    'Playing': 0,
    'Paused':  1,
    'Stopped': 2,
}


PLAYER_OBJECT_NAME = "/org/mpris/MediaPlayer2"
MAIN_INTERFACE_NAME = "org.mpris.MediaPlayer2"
PLAYER_INTERFACE_NAME = "org.mpris.MediaPlayer2.Player"

def get_sorted_candidate_buses():
    candidates = get_all_mpris_buses()
    # Sort by PlaybackStatus
    l = []
    import dbus
    for n in candidates:
        state = str(DBusProperties(n, PLAYER_OBJECT_NAME,
                                   PLAYER_INTERFACE_NAME).get("PlaybackStatus"))
        l.append((playback_status_levels[state], n))
    l.sort()
    return [n for i, n in l]


class Mpris2Player(Player):

    _friendly_name = "Any MPRIS 2 player"

    sort_order = 5

    @property
    def friendly_name(self):
        retval = self._friendly_name
        try:
            l = get_sorted_candidate_buses()
            names = []

            for n in l:
                try:
                    props = DBusProperties(n, PLAYER_OBJECT_NAME, MAIN_INTERFACE_NAME)
                    names.append(props.get("Identity"))
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
            obj = DBusObject(self.bus_name, PLAYER_OBJECT_NAME, PLAYER_INTERFACE_NAME)
            self._player = obj
            return obj

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
            bus = self.player._bus
            return True
        except dbus.DBusException:
            return False

    def is_paused(self):
        return self._playback_status() == "Paused"

    def is_stopped(self):
        return self._playback_status() == "Stopped"

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
        self.player.PlayPause()

    def next(self):
        self.player.Next()

    def prev(self):
        self.player.Previous()

    def stop(self):
        self.player.Stop()

    def osd(self):
        raise NotImplementedError()
