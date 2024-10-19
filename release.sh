#!/bin/sh

umask 000
rm -rf build dist
git ls-tree --full-tree --name-only -r HEAD | xargs chmod ugo+r
find src -type d | xargs chmod ugo+rx

uv build --sdist --wheel || exit 1
uv publish --sdist --wheel  || exit 1

VERSION=$(uv pip show playerdo | grep 'Version: ' | cut -f 2 -d ' ' | tr -d '\n') || exit 1

git tag $VERSION || exit 1
git push || exit 1
git push --tags || exit 1
