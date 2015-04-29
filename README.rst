Student Robotics Tools
======================

Installation
------------

.. code:: shell

    $ pip install --user .

Running
-------

Make sure ``~/.local/bin`` is in your PATH.

.. code:: shell

    $ sr --help

Documentation
-------------

Unfortunately there doesn’t appear to be a simple way of build ``man`` pages
and installing them via ``Setuptools``. Instead you should run ``./setup.py
build_sphinx`` and then copy them from ``build/sphinx/man`` to your manpage
directory.
