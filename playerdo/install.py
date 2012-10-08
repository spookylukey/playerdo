"""
Installation utilities for keyboard shortcuts
"""
from subprocess import Popen, PIPE, call
import sys


def force_unicode(s):
    if type(s) is not unicode:
        return s.decode('UTF-8')
    else:
        return s


class GnomeSettingsInstallerBase(object):

    def install_shortcuts(self):
        already_installed = set()
        max_count = 0
        for d in self.get_keybindings():
            if d.startswith('custom'):
                action = self.get_gconf_val(self.KEYBINDINGS_CONF_PREFIX + "/" + d + "/action")
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
                self.install_action("custom%d" % n, action, name)
                n += 1

    def get_keybindings(self):
        try:
            p = Popen([self.CONF_TOOL, "--all-dirs", self.KEYBINDINGS_CONF_PREFIX], stdout=PIPE)
        except OSError:
            raise Exception("Could not use %s to manipulate settings" % self.CONF_TOOL)
        stdout, stderr = p.communicate(None)
        if p.returncode != 0:
            raise Exception("Could not use %s to manipulate settings" % self.CONF_TOOL)
        retval = []
        stdout = force_unicode(stdout)
        for x in stdout.split("\n"):
            x = x.strip()
            if x.startswith(self.KEYBINDINGS_CONF_PREFIX):
                retval.append(x[len(self.KEYBINDINGS_CONF_PREFIX) + 1:])
        return retval

    def install_action(self, keybinding_name, action, name):
        self.set_gconf_val(self.KEYBINDINGS_CONF_PREFIX + "/" + keybinding_name + "/" + "action", action)
        self.set_gconf_val(self.KEYBINDINGS_CONF_PREFIX + "/" + keybinding_name + "/" + "binding", "")
        self.set_gconf_val(self.KEYBINDINGS_CONF_PREFIX + "/" + keybinding_name + "/" + "name", name)
        sys.stdout.write("Keybinding slot for action '%s' created\n" % action)

    def get_gconf_val(self,  key):
        p = Popen([self.CONF_TOOL, "--get", key], stdout=PIPE)
        stdout, stderr = p.communicate(None)
        if p.returncode != 0:
            raise Exception("Could not use %s to manipulate settings" % self.CONF_TOOL)
        return force_unicode(stdout)


    def set_gconf_val(self, key, val):
        p = Popen([self.CONF_TOOL, "--type", "string", "--set", key, val], stdout=PIPE)
        stdout, stderr = p.communicate(None)
        if p.returncode != 0:
            raise Exception("Could not use %s to manipulate settings" % self.CONF_TOOL)

    def launch_keybinding_editor(self):
        sys.stdout.write("Launching keybinding editor...\nEdit 'player_do' keybindings in 'Custom shortcuts' section, and close when done.\n")
        errors = []
        success = False
        p = Popen(["which", self.KEYBINDINGS_GUI_EDITOR], stdout=PIPE)
        stdout, stderr = p.communicate(None)
        val = force_unicode(stdout).strip()
        if val != "":
            call(["nohup %s &" % val], shell=True, stdout=open("/dev/null"), stderr=open("/dev/null"))
            success = True
        if not success:
            sys.stdout.write("Error: Couldn't find program %s for editing keybindings.\n" % self.KEYBINDINGS_GUI_EDITOR)
            raise SystemExit()


class GnomeSettingsInstaller(GnomeSettingsInstallerBase):
    CONF_TOOL = "gconftool-2"
    KEYBINDINGS_CONF_PREFIX = "/desktop/gnome/keybindings"
    KEYBINDINGS_GUI_EDITOR = "gnome-keybinding-properties"


class MateSettingsInstaller(GnomeSettingsInstallerBase):
    CONF_TOOL = "mateconftool-2"
    KEYBINDINGS_CONF_PREFIX = "/desktop/mate/keybindings"
    KEYBINDINGS_GUI_EDITOR = "mate-keybinding-properties"


def mk_installer(cls):
    def installer():
        i = cls()
        i.install_shortcuts()
        i.launch_keybinding_editor()
    return installer

install_gnome = mk_installer(GnomeSettingsInstaller)
install_mate = mk_installer(MateSettingsInstaller)
