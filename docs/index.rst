.. -*- coding: utf-8; mode: rst -*-
.. include:: refs.txt

.. _sphinx-xelatex-doc:

==============
Sphinx-XeLaTeX
==============

.. automodule:: xelatex_ext
    :members:
    :undoc-members:
    :show-inheritance:


Documentation
=============

.. toctree::
   :maxdepth: 1

   install


About
=====

This modul brings a *native* XeLaTeX builder and writer to the Sphinx
documentation generator. The XeLaTeX output is suited for processing with
XeLaTeX (http://tug.org/xetex/).

There has been a XeLaTeX support in Sphinx (and docutils) already, but this
inherits from (is based on) LaTeX implementations. XeLaTeX has builtin
unicode support, uses ``fontspec`` and ``polyglossia``, while LaTeX needs
``inputenc``, additional unicode declaration and uses ``babel`` for
hyphenation. In short, XeLaTeX and ``polyglossia`` are making things much
simpler. XeLaTeX have similarities, but a XeLateX generator should not
inherited or based on a LaTeX implementation.

The XeLaTeX builder (and writer) is a rewrite from scratch which tries to
keep as many as possible similarities to the to the Sphinx LaTeX and
docutils XeTeX builder:

* https://github.com/sphinx-doc/sphinx/tree/master/sphinx

and the sources of the docutils XeTeX writer:

* http://docutils.sourceforge.net/docutils/writers/xetex


Source Code Documentation
=========================

.. toctree::
   :maxdepth: 2

   xelatex/xelatex_ext


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
