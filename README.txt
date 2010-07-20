player_do
=========

I use several media players, sometimes at the same time (like 'shell-fm' running
in a terminal, and something else with a GUI), and sometimes I try out new media
players for a while. I want the the media buttons on my keyboard to Do The Right
Thing without having to reprogram keyboard shortcuts.  This package is my
solution to that problem.

I set up keyboard shortcuts to map the play/pause button to 'player_do
playpause' etc, and player_do generally does the Right Thing.

The currently supported programs can be seen by running 'player_do help'.  To
add more supported programs, see the existing code in the 'backends' directory.
Patches gratefully received!

Many players support the MPRIS DBUS protocol, and will be supported without
a specific backend.  If you only need support for those players, consider
using `MPRIS-remote <http://incise.org/mpris-remote.html>`_.
