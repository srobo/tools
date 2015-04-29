Installation
============

Methods
-------

There are two tried and tested methods of installing the tools.


Pip
~~~

The recommended and 'official' way of installing the tools is to use Pip.

.. code::

    $ pip install git+git://srobo.org/tools.git

You may also choose to install the tools locally with the ``--user`` option.
You should make sure that ``~/.local/bin`` is in your ``PATH`` variable if you
choose to do that.

Setuptools
~~~~~~~~~~

Using Setuptools to install the tools is more common if you are going to make
changes to the tools.

.. code::

    $ git clone git://srobo.org/tools.git
    $ cd tools
    $ ./setup install

As with Pip, there is a ``--user`` flag available if you want to install the
tools locally.

Dependencies
------------

If you wish to install the dependencies yourself rather than relying on ``Pip``
or ``Setuptools`` to do so for you, perhaps to use a system–wide package
manager, you should install the following packages.

- pyyaml
- sympy
- pyparsing
- beautifulsoup4
- numpy
- six
- tabulate
- xlwt-future
- pyudev
- matplotlib
- keyring

.. note:: Some packages are optional and other tools will work without them
          installed. If a specific tool requires a package to be available, a
          friendly error message shall be displayed.

Virtual Environments
--------------------

The tools work fine in virtual environments and using them is recommended
if you intend on making changes.

.. code::

    $ git clone git://srobo.org/tools.git
    $ cd tools
    $ pyvenv venv
    $ source venv/bin/activate
    $ pip install -e .

If all went well, you will have an ``sr`` binary available for you in the
``venv`` directory. It should also be in your ``PATH`` environment variable.

.. note:: By using ``-e``, the package is symbolically linked into the Python
          ``site-packages`` directory meaning that any changes in the source
          are reflected immediately.
