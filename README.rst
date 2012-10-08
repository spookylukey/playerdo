player_do provides a simple command line interface to control whatever media
player is running on your computer.

It is designed to allow you to configure the media buttons on your keyboard
(play, pause, next etc.) to Do The Right Thing without having to change anything
if you switch to a different media player.

It also includes commands 'install_gnome','install_mate', and 'install_gnome3'
to help set up keyboard shortcuts initially on GNOME2/Mate/GNOME3/Cinnamon. It
can, however, be used with any system where you can map keyboard shortcuts to
commands.

The currently supported media players can be seen by running 'player_do
help'. Those that have been tested include the following:

* Audacious
* Amarok
* Banshee
* Clementine
* cmus
* Exaile
* Guayadeque
* moc
* Quodlibet
* Rhythmbox
* shell-fm
* VLC (2.0 and later)

Many other players will be supported due to support for the MPRIS DBUS protocol,
without a specific backend.  If you only need support for those players,
consider using `MPRIS-remote <http://incise.org/mpris-remote.html>`_.

To add more supported programs, see the existing code in the 'backends'
directory.  Patches gratefully received!

Source code: http://bitbucket.org/spookylukey/playerdo/src

Bug tracking: http://bitbucket.org/spookylukey/playerdo/issues
