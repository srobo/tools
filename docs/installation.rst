Installation
============

There are two tried and tested methods of installing the tools.

With Pip
---------

The recommended and 'official' way of installing the tools is to use Pip.

.. code::

    $ pip install git+git://srobo.org/tools.git

You may also choose to install the tools locally with the ``--user`` option.
You should make sure that ``~/.local/bin`` is in your ``PATH`` variable if you
choose to do that.

With Setuptools
---------------

Using Setuptools to install the tools is more common if you are going to make
changes to the tools.

.. code::

    $ git clone git://srobo.org/tools.git
    $ cd tools
    $ ./setup install

As with Pip, there is a ``--user`` flag available if you want to install the
tools locally.

Virtual Environments
--------------------

The tools work fine in virtual environments and using them is recommended
if you intend on making changes.

.. code::

    $ git clone git://srobo.org/tools.git
    $ cd tools
    $ pyvenv venv
    $ source venv/bin/activate
    $ ./setup.py develop

If all went well, you will have an ``sr`` binary available for you in the
``venv`` directory. It should also be in your ``PATH`` environment variable.

By using ``develop`` instead of ``install``, the package is symlinked into the
Python ``site-packages`` directory meaning that any changes in the source are
reflected immediately.
