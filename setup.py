#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import sys

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

    import distutils.util
    import setuptools
    from lib2to3.refactor import get_fixers_from_package
    fixer_names = []
    for p in setuptools.lib2to3_fixer_packages:
        fixer_names.extend(get_fixers_from_package(p))

    # Modify
    fixer_names.remove('lib2to3.fixes.fix_next')
    # Monkey patch:
    distutils.util.Mixin2to3.fixer_names = fixer_names

setup(
    name = "playerdo",
    version = "0.5.2",
    packages = find_packages(),
    include_package_data = True,
    scripts = ['player_do'],

    # metadata for upload to PyPI
    author = "Luke Plant",
    author_email = "L.Plant.98@cantab.net",
    description = "Control various media players from a single command line interface.",
    long_description = (
                        read('README.rst')
                        + "\n\n" +
                        read('CHANGES.rst')
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
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        ],
    **extra
)


# dbus isn't on PyPI, can't just put it in requirements
try:
    import dbus
except ImportError:
    sys.stderr.write("WARNING: Python 'dbus' library is not installed. Some backends will not work.\n")
    if sys.version_info >= (3,):
        sys.stderr.write("At the time of writing, a Python 3 dbus library is only available if you build the py3k branch available at http://cgit.freedesktop.org/dbus/dbus-python/ \n")
