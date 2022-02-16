#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import sys


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


extra = {}

setup(
    name="playerdo",
    version="2.0.1",
    packages=find_packages(),
    include_package_data=True,
    scripts=['player_do'],
    python_requires=">=3.2",
    # metadata for upload to PyPI
    author="Luke Plant",
    author_email="L.Plant.98@cantab.net",
    description="Control various media players from a single command line interface.",
    long_description=(
        read('README.rst')
        + "\n\n" +
        read('CHANGES.rst')
    ),
    license="BSD",
    keywords="music media MPRIS player command interface wrapper",
    url="http://bitbucket.org/spookylukey/playerdo",
    classifiers=[
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        ],
    **extra
)


# dbus isn't on PyPI, can't just put it in requirements
try:
    import dbus  # noqa
except ImportError:
    sys.stderr.write("WARNING: Python 'dbus' library is not installed. Some backends will not work.\n")
