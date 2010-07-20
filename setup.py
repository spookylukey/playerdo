#!/usr/bin/env python
from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name = "playerdo",
    version = "0.2",
    packages = find_packages(),
    scripts = ['player_do'],

    # metadata for upload to PyPI
    author = "Luke Plant",
    author_email = "L.Plant.98@cantab.net",
    description = "Control various media players from a single command line interface.",
    long_description = (
                        read('README.txt')
                        + "\n\n" +
                        read('CHANGES.txt')
    ),
    license = "BSD",
    keywords = "music media MPRIS player command interface wrapper",
    url = "http://bitbucket.org/spookylukey/playerdo",
    classifiers = [
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: POSIX :: Linux",
        ]
)
