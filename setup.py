#!/usr/bin/env python
# -*- coding: utf-8; mode: python -*-

# http://python-packaging.readthedocs.io

from setuptools import setup, find_packages
import xelatex_ext as pckg

install_requires = [
    'fspath'
    , 'six' ]

setup(
    name               = "linuxdoc"
    , version          = pckg.__version__
    , description      = pckg.__description__
    , long_description = pckg.__doc__
    , url              = pckg.__url__
    , author           = "Markus Heiser"
    , author_email     = "markus.heiser@darmarIT.de"
    , license          = pckg.__license__
    , keywords         = "xelatex sphinx extension"
    , packages         = find_packages(exclude=['docs', 'tests'])
    , install_requires = install_requires

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    , classifiers = [
        "Development Status :: 5 - Production/Stable"
        , "Intended Audience :: Developers"
        , "Intended Audience :: Other Audience"
        , "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
        , "Operating System :: OS Independent"
        , "Programming Language :: Python"
        , "Programming Language :: Python :: 2"
        , "Programming Language :: Python :: 3"
        , "Topic :: Utilities"
        , "Topic :: Documentation :: linux"
        , "Topic :: Software Development :: Documentation"
        , "Topic :: Software Development :: Libraries"
        , "Topic :: Text Processing" ]
)
