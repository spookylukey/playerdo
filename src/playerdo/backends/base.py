from playerdo.utils import catch_unimplemented, program_running


# Base class useful for implementing players
class Player:
    """
    Base class for implementing players.  It does not have to
    be used, but does provide some useful default behaviour.
    """

    process_name: str  # used for pidof
    friendly_name: str  # required, used for display in help and to identify concrete subclasses
    sort_order = 0  # set lower for higher priority

    @classmethod
    def get_instances(cls):
        # Most Players have a single instance.
        if cls.check_dependencies():
            return []
        return [cls()]

    def is_running(self):
        """
        Returns true if the player program is running.
        Must be implemented (or process_name must be specified)
        """
        if self.process_name is None:
            raise NotImplementedError
        return program_running(self.process_name)

    def is_stopped(self):
        """
        Returns True if the player is in a 'stopped' state (which does not
        include 'paused')
        """
        raise NotImplementedError

    def is_paused(self):
        """
        Returns True if the player is in a 'paused' state.
        """
        raise NotImplementedError

    @classmethod
    def check_dependencies(cls):
        """
        Returns a list of failed dependencies for using this backend, or an
        empty list if everything is OK.  Most players do not need this.
        """
        return []

    def do_command(self, command):
        try:
            m = getattr(self, command)
        except AttributeError:
            raise Exception(f"'{command}' is not a valid command")
        return m()

    # Commands
    def play(self):
        """
        Plays current track in media player.
        """
        raise NotImplementedError

    def pause(self):
        """
        Pauses current track in media player.
        """
        raise NotImplementedError

    def unpause(self):
        """
        Continues playing current track if paused.
        """
        raise NotImplementedError

    def togglepause(self):
        """
        Plays if paused, pauses if playing.
        """
        is_paused = catch_unimplemented(self.is_paused)

        if is_paused is True:
            self.unpause()
        elif is_paused is False:
            self.pause()
        else:
            # Just hope this does the right thing:
            self.pause()

    def playpause(self):
        """
        Plays if stopped/paused, pauses if playing.
        """
        is_stopped = catch_unimplemented(self.is_stopped)

        if is_stopped is True:
            self.play()
        elif is_stopped is False:
            self.togglepause()
        else:
            # Just hope 'togglepause' does the right thing:
            self.togglepause()

    def stop(self):
        """
        Stops playing.
        """
        raise NotImplementedError

    def next(self):
        """
        Plays next track.
        """
        raise NotImplementedError

    def prev(self):
        """
        Plays previous track.
        """
        raise NotImplementedError

    def osd(self):
        """
        Shows OSD (on screen display).
        """
        raise NotImplementedError

    def is_playing(self):
        """
        Returns True if the player is playing a song, False otherwise.
        """

    def __lt__(self, other):
        # This is needed to stop errors on Python 3
        return self.sort_order < other.sort_order
