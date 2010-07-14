from playerdo.backends.mpris import MprisPlayer


class Clementine(MprisPlayer):

    process_name = "clementine"
    bus_name = "org.mpris.clementine"
