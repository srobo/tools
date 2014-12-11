trac-deps-rm
============

Synopsis
--------

``sr trac-deps-rm [-h] [-m <message>] [--dry-run] <ticket> <dependency> [<dependency> ...]``

Description
-----------

Remove dependencies from a ticket.

Options
-------

--help, -h
    Display help and exit.

-m <message>
    A message to append to the dependency remove action.

--dry-run
    Do all processing but don't actually modify the ticket.

Examples
--------

.. code::

    $ sr trac-deps-rm 100 101 102
