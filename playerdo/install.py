"""
Installation utilities for keyboard shortcuts
"""
from subprocess import Popen, PIPE, call
import sys


KEYBINDINGS_PREFIX = "/desktop/gnome/keybindings"

def force_unicode(s):
    if type(s) is not unicode:
        return s.decode('UTF-8')
    else:
        return s

def install_gnome():
    """
    Creates stub keybindings for player_do commands in GNOME, and launches a GUI
    editor for the user to set keys.
    """
    already_installed = set()
    max_count = 0
    for d in get_gnome_keybindings():
        if d.startswith('custom'):
            action = get_gconf_val(KEYBINDINGS_PREFIX + "/" + d + "/action")
            if action.startswith("player_do "):
                already_installed.add(action.strip())
            n = int(d[len('custom'):])
            if n > max_count:
                max_count = n

    commands = ['play', 'pause', 'playpause', 'stop', 'next', 'prev']
    n = max_count + 1
    for cmd in commands:
        action = "player_do " + cmd
        name = "player_do - " + cmd
        if action not in already_installed:
            install_action("custom%d" % n, action, name)
            n += 1
    sys.stdout.write("Launching keybinding editor...\nEdit 'player_do' keybindings in 'Custom shortcuts' section, and close when done.\n")
    launch_keybinding_editor()


def get_gnome_keybindings():
    p = Popen(["gconftool-2", "--all-dirs", KEYBINDINGS_PREFIX], stdout=PIPE)
    stdout, stderr = p.communicate(None)
    if p.returncode != 0:
        raise Exception("Could not use gconftool to manipulate settings")
    retval = []
    stdout = force_unicode(stdout)
    for x in stdout.split("\n"):
        x = x.strip()
        if x.startswith(KEYBINDINGS_PREFIX):
            retval.append(x[len(KEYBINDINGS_PREFIX) + 1:])
    return retval


def get_gconf_val(key):
    p = Popen(["gconftool-2", "--get", key], stdout=PIPE)
    stdout, stderr = p.communicate(None)
    if p.returncode != 0:
        raise Exception("Could not use gconftool to manipulate settings")
    return force_unicode(stdout)


def set_gconf_val(key, val):
    p = Popen(["gconftool-2", "--type", "string", "--set", key, val], stdout=PIPE)
    stdout, stderr = p.communicate(None)
    if p.returncode != 0:
        raise Exception("Could not use gconftool to manipulate settings")


def install_action(keybinding_name, action, name):
    set_gconf_val(KEYBINDINGS_PREFIX + "/" + keybinding_name + "/" + "action", action)
    set_gconf_val(KEYBINDINGS_PREFIX + "/" + keybinding_name + "/" + "binding", "")
    set_gconf_val(KEYBINDINGS_PREFIX + "/" + keybinding_name + "/" + "name", name)
    sys.stdout.write("Keybinding slot for action '%s' created\n" % action)


def launch_keybinding_editor():
    p = Popen(["which", "gnome-keybinding-properties"], stdout=PIPE)
    stdout, stderr = p.communicate(None)
    val = force_unicode(stdout).strip()
    if val == "":
        raise Exception("Can't find program gnome-keybinding-properties to configure keys")
    call(["nohup %s &" % val], shell=True, stdout=open("/dev/null"), stderr=open("/dev/null"))
