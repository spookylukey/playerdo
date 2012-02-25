Change log
==========

Version 0.5.2
-------------

* Fixed incorrect use of MPRIS2 protocol that caused VLC 2.0 to crash.
  Thanks to Anonymous for the bug report and patch (tell me your name
  if you want it here!).

Version 0.5.1
-------------

* Fixed some Python 3 incompatibilities
* Fixed crash if DBus library is not installed
* Fixed support for newer version of Banshee

Version 0.5
-----------

* Added support for quodlibet
* Fixed support for Guayadeque

Version 0.4
-----------

* Added support for MPRIS2 players
* Added ``install_gnome`` command to help set up keyboard shortcuts on GNOME
* Eliminated dependency on shc.hs for the shell-fm backend
* Various bug fixes/optimisations

Version 0.3
-----------

* Fixed fatal packaging bug!
* Improved help text for MPRIS players (lists currently running players).
* Made dbus dependency optional
* Support for Python 3 via 2to3.

Version 0.2
-----------

* Added support for Banshee.
* Implemented 'test' command where needed.
* Small bug fixes.

Version 0.1
-----------

* Initial release.
* Support for any MPRIS player, shell-fm, mocp and rhythmbox.
