#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
    name = "playerdo",
    version = "0.1",
    packages = find_packages(),
    scripts = ['player_do'],

    # metadata for upload to PyPI
    author = "Luke Plant",
    author_email = "L.Plant.98@cantab.net",
    description = "Control various media players from a single command line interface.",
    license = "BSD",
    keywords = "music media MPRIS player command interface wrapper",
    url = "http://bitbucket.org/spookylukey/playerdo",
    classifiers = [
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta"
        ]
)
