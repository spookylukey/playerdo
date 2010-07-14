from playerdo.backends.mpris import MprisPlayer


class Amarok(MprisPlayer):

    process_name = "amarok"
    bus_name = "org.mpris.amarok"
