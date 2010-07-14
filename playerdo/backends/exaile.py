from playerdo.backends.mpris import MprisPlayer
from playerdo.utils import DBusObject


class Exaile(MprisPlayer):

    name = "Exaile"
    bus_name = "org.mpris.exaile"

    def is_stopped(self):
        exaile = DBusObject(self.bus_name, "/org/exaile/Exaile")
        return not bool(exaile.IsPlaying())
