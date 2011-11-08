
So you use several media players, sometimes at the same time (like 'shell-fm'
running in a terminal, and something else with a GUI), and sometimes you like to
try out new media players for a while. And you want the the media buttons on
your keyboard to Do The Right Thing without having to reprogram keyboard
shortcuts.  This package is a solution to that problem.

You can set up keyboard shortcuts to map the play/pause button to 'player_do
playpause' etc, and player_do generally does the Right Thing.

There is a command 'install_gnome' to help set up keyboard shortcuts on GNOME.

The currently supported programs can be seen by running 'player_do help'. Those
that have been tested include the following:

* Audacious
* Amarok
* Banshee
* Clementine
* Exaile
* Guayadeque
* moc
* Quodlibet
* Rhythmbox
* shell-fm

Many other players will be supported due to support for the MPRIS DBUS protocol,
without a specific backend.  If you only need support for those players,
consider using `MPRIS-remote <http://incise.org/mpris-remote.html>`_.

To add more supported programs, see the existing code in the 'backends'
directory.  Patches gratefully received!

Source code: http://bitbucket.org/spookylukey/playerdo/src

Bug tracking: http://bitbucket.org/spookylukey/playerdo/issues
