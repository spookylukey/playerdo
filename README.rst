player_do
=========

player_do provides a simple command line interface to control whatever media
player is running on your computer. It has been designed for and tested on
Linux.

It is designed to allow you to configure the media buttons on your keyboard
(play, pause, next etc.) to Do The Right Thing without having to change anything
if you switch to a different media player.

It also includes commands ``install_gnome``, ``install_mate``,
``install_gnome3``, and ``install_cinnamon`` to help set up keyboard shortcuts
initially on GNOME2/Mate/GNOME3/Cinnamon. It can, however, be used with any
system where you can map keyboard shortcuts to commands.

The currently supported media players can be seen by running ``player_do --help``.
Those that have been tested include the following:

* Audacious
* Amarok
* Banshee
* Clementine
* cmus
* Exaile
* Guayadeque
* moc
* MPD (configurable using MPD_HOST and MPD_PORT environment variables like mpc)
* pianobar
* Quodlibet
* Rhythmbox (needs MPRIS plugin installed and enabled)
* shell-fm (0.8 and later)
* VLC (2.0 and later)
* Firefox, Chrome (when playing some media like videos and podcasts)

Many other players will be supported due to support for the MPRIS DBUS protocol,
without a specific backend. If you only need support for those players, consider
using `MPRIS-remote <http://incise.org/mpris-remote.html>`_ or `playerctl
<https://github.com/altdesktop/playerctl>`_.

To add more supported programs, see the existing code in the ``backends``
directory. Patches gratefully received!

Installation
------------

You need Python 3.8 or later, Python 3.12 or later recommended as I test on
that. We recommend the use of `uv <https://docs.astral.sh/uv/>`_ to install as
below::

    uv python install 3.12
    uv tool install playerdo --python 3.12

This should install everything for you.

If an appropriate binary wheel for dbus is not found, the above may require
development packages to be installed, including ``libglib2.0-dev`` and
``libdbus-1-dev`` and Python development headers.


Installation using pipx
-----------------------

On older systems or if ``uv`` is not available, you can install using `pipx
<https://pypi.org/project/pipx/>`_ to install it into its own virtualenv, using
your standard system Python 3, like this::

  pipx install playerdo


Installation using pip
----------------------

If the above is problematic (due to difficulties compiling dbus, typically), you
can install using ``pip`` and a system copy of the ``dbus-python`` bindings.

on Debian Linux systems (including Ubuntu, Linuxmint etc), first do::

  sudo apt install python3-dbus

Then create a virtualenv for the installation, in a location of your choosing,
with the ``--system-site-packages`` option::

  python3 -m venv playerdo_venv --system-site-packages

Activate it::

  . playerdo_venv/bin/activate

Install playerdo without dependencies::

  pip install --no-deps playerdo

Check it is installed::

  playerdo --help

Check dbus bindings are found - the following should print nothing::

  playerdo test

The following prints the full path to where you’ve installed id::

  which playerdo

Usage
-----

Control the currently active player using commands like::

  player_do playpause
  player_do next


For all commands and other options, see::

  player_do --help



Links
-----
Download: https://pypi.python.org/pypi/playerdo

Source code: https://github.com/spookylukey/playerdo

Bug tracking: https://github.com/spookylukey/playerdo/issues

Changes: https://github.com/spookylukey/playerdo/blob/master/CHANGES.rst
