
So you use several media players, sometimes at the same time (like 'shell-fm'
running in a terminal, and something else with a GUI), and sometimes you like to
try out new media players for a while. And you want the the media buttons on
your keyboard to Do The Right Thing without having to reprogram keyboard
shortcuts.  This package is a solution to that problem.

You can set up keyboard shortcuts to map the play/pause button to 'player_do
playpause' etc, and player_do generally does the Right Thing.

There is a command 'install_gnome' to help set up keyboard shortcuts on GNOME.

The currently supported programs can be seen by running 'player_do help'.  To
add more supported programs, see the existing code in the 'backends' directory.
Patches gratefully received!

Many players support the MPRIS DBUS protocol, and will be supported without
a specific backend.  If you only need support for those players, consider
using `MPRIS-remote <http://incise.org/mpris-remote.html>`_.

Source code: http://bitbucket.org/spookylukey/playerdo/src

Bug tracking: http://bitbucket.org/spookylukey/playerdo/issues
