trac-attach
===========

Synopsis
--------

``sr trac-attach [-h] [-s <server>] [-p <port>] [-d <description>] <ticket> <filename>``

Description
-----------

Attach a file to a Trac ticket.

Options
-------

--help, -h
    Display help and exit.

--server <server>, -s <server>
    Hostname of the server to talk to.

--port <port>, -p <port>
    Port of the server to talk to.

--desc <description>, -d <description>
    The description of the file.

Examples
--------

.. code::

    $ sr trac-attach 545 tallship_b.jpg
