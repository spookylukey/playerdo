from playerdo.utils import program_running, catch_unimplemented

# Base class useful for implementing players
class Player(object):

    process_name = None

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

    def do_command(self, command):
        try:
            m = getattr(self, command)
        except AttributeError:
            raise Exception("'%s' is not a valid command" % command)
        return m()

    # Commands
    def play(self):
        raise NotImplementedError

    def pause(self):
        raise NotImplementedError

    def unpause(self):
        raise NotImplementedError

    def togglepause(self):
        """
        Play if paused, pause if playing
        """
        is_paused = catch_unimplemented(self.is_paused)

        if is_paused == True:
            self.unpause()
        elif is_paused == False:
            self.pause()
        else:
            # Just hope this does the right thing:
            self.pause()

    def playpause(self):
        """
        Play if stopped/paused, pause if playing
        """
        is_stopped = catch_unimplemented(self.is_stopped)

        if is_stopped == True:
            self.play()
        elif is_stopped == False:
            self.togglepause()
        else:
            # Just hope 'togglepause' does the right thing:
            self.togglepause()

    def stop(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

    def prev(self):
        raise NotImplementedError

    def osd(self):
        raise NotImplementedError

