Release process
---------------

* Update the version in setup.py

* Release::

    $ ./release.sh

* Tag the release e.g.::

    $ git tag 1.2.0
    $ git push upstream master --tags
