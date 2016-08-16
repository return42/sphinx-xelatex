.. -*- coding: utf-8; mode: rst -*-
.. include:: refs.txt

.. _install_sphinx-xelatex:

=======
Install
=======

Install bleeding edge::

  pip install --user git+http://github.com/return42/sphinx-xelatex.git

or clone from github::

  git clone https://github.com/return42/sphinx-xelatex.git
  cd sphinx-xelatex
  make install

As the project WIP , an update should be carried out regularly.::

  pip install --upgrade git+http://github.com/return42/sphinx-xelatex.git

If you are a developer and like to contribute to the project, fork on github or
clone and make a developer install::

  git clone https://github.com/return42/sphinx-xelatex
  cd sphinx-xelatex
  make install

Below you see how to integrate the sphinx extensions into your sphinx build
process. In the ``conf.py`` (`sphinx config`_) add the ``xelatex_ext``
extension:

.. code-block:: python

   extensions = [ ... 'xelatex_ext' ]

