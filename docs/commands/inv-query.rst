inv-query
=========

Synopsis
--------

``sr inv-query [-h] [--codes] [--paths] [-v] <query>``

Description
-----------

Run a query on the inventory.

.. include:: ../inventory/queries.inc.rst

Options
-------

--help, -h
    Display help and exit.

--codes
    Display the results as a list of asset codes.

--paths
    Display the results as a list of paths.

-v
    Enable verbose mode.

Examples
--------

.. code::

    $ sr inv-query code:N1V36
    /.../teams/2015/crb/box-18l-rub-sr0G64/webcam-logitech-c270-srN1V36
