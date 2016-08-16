# -*- coding: utf-8; mode: python -*-
# pylint: disable=R0912, R0903, C0330

u"""
This modul brings a *native* XeLaTeX builder and writer to the Sphinx
documentation generator. The XeLaTeX output is suited for processing with
XeLaTeX (http://tug.org/xetex/).

:copyright:  Copyright (C) 2016 Markus Heiser
:e-mail:     *markus.heiser*\ *@*\ *darmarIT.de*
:license:    GPL Version 2, June 1991 see Linux/COPYING for details.
:docs:       http://return42.github.io/sphinx-xelatex
:repository: `github return42/linuxdoc <https://github.com/return42/sphinx-xelatex>`_
"""

__version__     = "00000000"
__copyright__   = "2016 Markus Heiser"
__url__         = "http://return42.github.io/sphinx-xelatex"
__description__ = "Native XeLaTeX builder and writer for Sphinx-Doc"
__license__     = "GPLv2"

# ==============================================================================
#  imports ...
# ==============================================================================

from xelatex_ext.builders.xelatex import XeLaTeXBuilder

# ==============================================================================
def setup(app):
# ==============================================================================

    u"""initialize *this* sphinx extension"""

    app.add_builder(XeLaTeXBuilder)
    app.add_config_value("xelatex_documents", [], '')

