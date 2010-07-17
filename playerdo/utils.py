import subprocess
import dbus


# Helpers for process output
def process_stdout(args, input=None):
    """
    Executes the process with the commandline specified in 'args' and returns
    the standard output
    """
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    retval = p.communicate(input=input)[0]
    try:
        p.terminate()
    except OSError:
        pass
    return retval


def process_retval(args, input=None):
    """
    Executes the process with the commandline specified in 'args' and returns
    the return value
    """
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    p.communicate(input=input)
    return p.returncode


def process_true(args, input=None):
    """
    Executes a process and rturns true if the process has a zero return code
    """
    return process_retval(args, input=input) == 0


def program_running(progam):
    return process_true(["pidof", progam])


# DBus helpers
class DBusObject(object):
    """
    Wrapper for a dbus object, so that the bus name and object name only needs
    to be specified once.
    """

    def __init__(self, bus_name, object_name):
        bus = dbus.SessionBus()
        self._bus = bus
        self._obj = bus.get_object(bus_name, object_name)

    def __getattr__(self, name):
        def f(*args, **kwargs):
            return getattr(self._obj, name)(*args, **kwargs)
        return f


# Misc helpers
def catch_unimplemented(c, replacement=None):
    """
    Execute a callable c, returning replacement if it throws
    NotImplementedError
    """
    try:
        return c()
    except NotImplementedError:
        return replacement


class PlayerException(Exception):
    """
    An exception that should be handled nicely by the front end
    """

    def __init__(self, message):
        self.message = message
