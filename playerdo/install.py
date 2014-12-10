"""
Installation utilities for keyboard shortcuts
"""
from subprocess import Popen, PIPE, call
import sys


if sys.version_info.major > 2:
    unicode = str


def force_unicode(s):
    if type(s) is not unicode:
        return s.decode('UTF-8')
    else:
        return s


class SettingsInstallerBase(object):

    def get_next_custom_keybinding_name(self, existing):
        # All custom keybindings start with 'custom'
        if len(existing) == 0:
            next_val = 0
        else:
            next_val = max(int(n[len('custom'):]) for n in existing) + 1
        return 'custom' + str(next_val)

    def install_shortcuts(self):
        already_installed = set()
        custom_keybindings = set(self.get_custom_keybindings())
        for d in custom_keybindings:
            action = self.get_keybinding_action(d)
            if action.startswith("player_do "):
                already_installed.add(action.strip())

        commands = ['play', 'pause', 'playpause', 'stop', 'next', 'prev']
        for cmd in commands:
            action = "player_do " + cmd
            display_name = "player_do - " + cmd
            if action not in already_installed:
                keybinding_name = self.get_next_custom_keybinding_name(custom_keybindings)
                self.install_keybinding(keybinding_name, action, display_name)
                custom_keybindings.add(keybinding_name)

    def launch_keybinding_editor(self):
        sys.stdout.write("Launching keybinding editor...\nEdit 'player_do' keybindings in 'Custom shortcuts' section, and close when done.\n")
        success = False
        p = Popen(["which", self.KEYBINDINGS_GUI_EDITOR], stdout=PIPE)
        stdout, stderr = p.communicate(None)
        val = force_unicode(stdout).strip() + " " + " ".join(self.KEYBINDINGS_GUI_EDITOR_ARGS)
        if val != "":
            call(["nohup %s &" % val], shell=True, stdout=open("/dev/null"), stderr=open("/dev/null"))
            success = True
        if not success:
            sys.stdout.write("Error: Couldn't find program %s for editing keybindings.\n" % self.KEYBINDINGS_GUI_EDITOR)
            raise SystemExit()


class Gnome2SettingsInstallerBase(SettingsInstallerBase):

    def get_custom_keybindings(self):
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
                x = x[len(self.KEYBINDINGS_CONF_PREFIX) + 1:]
                if x.startswith("custom"):
                    retval.append(x)
        return retval

    def get_keybinding_action(self, keybinding_name):
        return self.get_gconf_val(self.KEYBINDINGS_CONF_PREFIX + "/" + keybinding_name + "/action")

    def install_keybinding(self, keybinding_name, action, display_name):
        self.set_gconf_val(self.KEYBINDINGS_CONF_PREFIX + "/" + keybinding_name + "/" + "action", action)
        self.set_gconf_val(self.KEYBINDINGS_CONF_PREFIX + "/" + keybinding_name + "/" + "binding", "")
        self.set_gconf_val(self.KEYBINDINGS_CONF_PREFIX + "/" + keybinding_name + "/" + "name", display_name)
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


class Gnome2SettingsInstaller(Gnome2SettingsInstallerBase):
    CONF_TOOL = "gconftool-2"
    KEYBINDINGS_CONF_PREFIX = "/desktop/gnome/keybindings"
    KEYBINDINGS_GUI_EDITOR = "gnome-keybinding-properties"
    KEYBINDINGS_GUI_EDITOR_ARGS = []


class MateSettingsInstaller(Gnome2SettingsInstallerBase):
    CONF_TOOL = "mateconftool-2"
    KEYBINDINGS_CONF_PREFIX = "/desktop/mate/keybindings"
    KEYBINDINGS_GUI_EDITOR = "mate-keybinding-properties"


class Gnome3SettingsInstallerBase(SettingsInstallerBase):
    """
    Common functionality between Gnome3 and Cinnamon
    """
    CONF_TOOL = "gsettings"

    def get_custom_keybindings(self):
        l = self.get_gsettings_val(self.KEYBINDINGS_SCHEMA, None, self.KEYBINDINGS_LIST_CUSTOM_KEY)
        retval = []
        for i in l:
            retval.append(self.get_custom_keybinding_working_name(i))
        return retval

    def get_keybinding_action(self, keybinding_name):
        return self.get_gsettings_val(self.KEYBINDINGS_SCHEMA_CUSTOM,
                                      self.keybinding_path(keybinding_name),
                                      "command")

    def install_keybinding(self, keybinding_name, action, display_name):
        self.set_gsettings_val(self.KEYBINDINGS_SCHEMA_CUSTOM,
                               self.keybinding_path(keybinding_name), "command", action)
        self.set_gsettings_val(self.KEYBINDINGS_SCHEMA_CUSTOM,
                               self.keybinding_path(keybinding_name), "name", display_name)
        self.set_gsettings_val(self.KEYBINDINGS_SCHEMA_CUSTOM,
                               self.keybinding_path(keybinding_name), "binding", self.empty_binding_val())

        # Update the list key
        l = self.get_custom_keybindings() # list like ['custom0', 'custom1']
        l.append(keybinding_name)
        self.set_gsettings_val(self.KEYBINDINGS_SCHEMA, None,
                               self.KEYBINDINGS_LIST_CUSTOM_KEY,
                               [self.get_custom_keybinding_stored_value(n) for n in l]
                               )

        sys.stdout.write("Keybinding slot for action '%s' created\n" % action)

    def keybinding_path(self, name):
        return self.KEYBINDINGS_CUSTOM_KEY_PATH + name + '/'

    def get_gsettings_val(self, schema, path, key):
        arg = schema
        if path:
            arg = arg + ":" + path
        p = Popen([self.CONF_TOOL, "get", arg, key], stdout=PIPE)
        stdout, stderr = p.communicate(None)
        if p.returncode != 0:
            raise Exception("Could not use %s to manipulate settings" % self.CONF_TOOL)
        v = force_unicode(stdout)

        return decode_gsettings(v)

    def set_gsettings_val(self, schema, path, key, val):
        arg = schema
        if path:
            arg = arg + ":" + path
        p = Popen([self.CONF_TOOL, "set", arg, key, force_unicode(encode_gsettings(val))], stdout=PIPE)
        stdout, stderr = p.communicate(None)
        if p.returncode != 0:
            raise Exception("Could not use %s to manipulate settings" % self.CONF_TOOL)

    def get_custom_keybinding_working_name(self, stored_value):
        raise NotImplementedError()

    def get_custom_keybinding_stored_value(self, working_name):
        raise NotImplementedError()


class Gnome3SettingsInstaller(Gnome3SettingsInstallerBase):
    KEYBINDINGS_GUI_EDITOR = "gnome-control-center"
    KEYBINDINGS_GUI_EDITOR_ARGS = ["keyboard"]

    KEYBINDINGS_SCHEMA = "org.gnome.settings-daemon.plugins.media-keys"
    KEYBINDINGS_LIST_CUSTOM_KEY = "custom-keybindings"
    KEYBINDINGS_SCHEMA_CUSTOM = "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding"
    KEYBINDINGS_CUSTOM_KEY_PATH = '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/'

    # Gnome3 stores
    # ['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/'...]
    # in the 'custom-keybindings' key

    def get_custom_keybinding_working_name(self, stored_value):
        assert stored_value.startswith(self.KEYBINDINGS_CUSTOM_KEY_PATH)
        val = stored_value.split('/')[-2]
        assert val.startswith('custom')
        return val

    def get_custom_keybinding_stored_value(self, name):
        return self.keybinding_path(name)

    def empty_binding_val(self):
        return ""


class CinnamonSettingsInstallerBase(Gnome3SettingsInstallerBase):
    KEYBINDINGS_GUI_EDITOR = "cinnamon-settings"
    KEYBINDINGS_GUI_EDITOR_ARGS = ["keyboard"]

    KEYBINDINGS_LIST_CUSTOM_KEY = "custom-list"

    # Cinnamon just stores 'custom0', 'custom1' in the 'custom-list' key
    def get_custom_keybinding_working_name(self, stored_value):
        return stored_value

    def get_custom_keybinding_stored_value(self, name):
        return name

class Cinnamon1SettingsInstaller(CinnamonSettingsInstallerBase):
    KEYBINDINGS_SCHEMA = "org.cinnamon.keybindings"
    KEYBINDINGS_SCHEMA_CUSTOM = "org.cinnamon.keybindings.custom-keybinding"
    KEYBINDINGS_CUSTOM_KEY_PATH = "/org/cinnamon/keybindings/custom-keybindings/"

    def empty_binding_val(self):
        return ""


class Cinnamon2SettingsInstaller(CinnamonSettingsInstallerBase):
    KEYBINDINGS_SCHEMA = "org.cinnamon.desktop.keybindings"
    KEYBINDINGS_SCHEMA_CUSTOM = "org.cinnamon.desktop.keybindings.custom-keybinding"
    KEYBINDINGS_CUSTOM_KEY_PATH = "/org/cinnamon/desktop/keybindings/custom-keybindings/"

    def empty_binding_val(self):
        return []


class CinnamonSettingsInstaller(object):
    installers = [Cinnamon1SettingsInstaller(), Cinnamon2SettingsInstaller()]

    def install_shortcuts(self):
        # This does both Cinnamon 1 and Cinnamon 2, which should cover our
        # bases.
        for i in self.installers:
            i.install_shortcuts()

    def launch_keybinding_editor(self):
        # They do the same thing, either will do
        self.installers[0].launch_keybinding_editor()


def decode_gsettings(v):
    # Looks like some Python based syntax
    if v.startswith('@as []'):
        return []
    else:
        return eval(v)


def encode_gsettings(v):
    return repr(v)


def mk_installer(cls):
    def installer():
        i = cls()
        i.install_shortcuts()
        i.launch_keybinding_editor()
    return installer

install_gnome = mk_installer(Gnome2SettingsInstaller)
install_mate = mk_installer(MateSettingsInstaller)
install_gnome3 = mk_installer(Gnome3SettingsInstaller)
install_cinnamon = mk_installer(CinnamonSettingsInstaller)
