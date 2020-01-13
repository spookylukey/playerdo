Change log
==========

Version 2.0 (2020-01-13)
------------------------
* Dropped Python 2 support
* Fixed some Python 3 issues


Version 1.0 (2019-06-16)
------------------------

* Support for pianobar
* Support for MPD.
* Better support for Cinnamon
* Fixed support for cmus

Version 0.9
-----------

* New 'install_cinnamon' command to properly support Cinnamon 2.0 and higher.
* Fixed some Python 3 compatibility issues, dropped support for Python < 2.7

Version 0.8
-----------

* new command 'is_playing'.
* shell-fm support now requires version 0.8

Version 0.7
-----------

* Added support for installing shortcuts in Mate and GNOME3/Cinnamon

Version 0.6.1
-------------

* Fixed small bug introduced in 0.6

Version 0.6
-----------

* Added support for cmus

Version 0.5.2
-------------

* Fixed incorrect use of MPRIS2 protocol that caused VLC 2.0 to crash.
  Thanks to orbisvicis for the very helpful bug report and patch.

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
