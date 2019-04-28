.. _install:

Installation of Habu
========================

This part of the documentation covers the installation of Habu.
The first step to using any software package is getting it properly installed.

$ pipenv install habu
---------------------

To install Habu, simply run this simple command in your terminal of choice::

    $ pipenv install habu

If you don't have `pipenv <http://pipenv.org/>`_ installed, head over to the
Pipenv website for installation instructions. Or, if you prefer to just use
pip and don't have it installed, `this Python installation guide <https://docs.python-guide.org/starting/installation/>`_
can guide you through the process.

Get the Source Code
-------------------

Habu is actively developed on GitHub, where the code is
`always available <https://github.com/portantier/habu>`_.

You can either clone the public repository::

    $ git clone git://github.com/portantier/habu

Or, download the `tarball <https://github.com/portantier/habu/tarball/master>`_::

    $ curl -OL https://github.com/portantier/habu/tarball/master
    # optionally, zipball is also available (for Windows users).

Once you have a copy of the source, you can embed it in your own Python
package, or install it into your site-packages easily::

    $ cd habu
    $ pip install .
