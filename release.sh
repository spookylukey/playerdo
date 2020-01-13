#!/bin/sh

umask 000
rm -rf build dist
git ls-tree --full-tree --name-only -r HEAD | xargs chmod ugo+r
find player_do -type d | xargs chmod ugo+rx

./setup.py sdist bdist_wheel || exit 1

VERSION=$(./setup.py --version) || exit 1

twine upload dist/playerdo-$VERSION-py2.py3-none-any.whl dist/playerdo-$VERSION.tar.gz
