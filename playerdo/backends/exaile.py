from playerdo.backends.mpris import MprisPlayer
from playerdo.utils import DBusObject


class Exaile(MprisPlayer):

    process_name = "exaile"
    bus_name = "org.mpris.exaile"

    def is_stopped(self):
        exaile = DBusObject(self.bus_name, "/org/exaile/Exaile")
        return not bool(exaile.IsPlaying())
