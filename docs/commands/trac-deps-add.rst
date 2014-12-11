trac-deps-add
=============

Synopsis
--------

``sr trac-deps-add [-h] [-m <message>] [--dry-run] <ticket> <dependency> [<dependency> ...]``

Description
-----------

Add dependencies to a ticket.

Options
-------

--help, -h
    Display help and exit.

-m <message>
    A message to append to the dependency add action.

--dry-run
    Do all processing but don't actually modify the ticket.

Examples
--------

.. code::

    $ sr trac-deps-add 100 101 102
