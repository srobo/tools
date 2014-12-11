make-purchase
=============

Synopsis
--------

``sr make-purchase [-h] [-s <server>] [-p <port>] [-f <spend_file>] [--dry-run]``

Description
-----------

Make a purchase on Trac.

Must be run from a ``spending.git`` clone.

Options
-------

--help, -h
    Display help and exit.

--server <server>, -s <server>
    The server hostname to talk to, defaults to the Student Robotics server.

--port <port>, -p <port>
    The server port to talk to, defaults to the Student Robotics server.

--spend-file <file>, -f <file>
    Specify a spending file directly. If this is not specified, your editor
    will open with an empty spending file for you to input the values directly.

--dry-run
    Perform all the processing, but don't actually create the purchasing
    ticket.

Examples
--------

.. code::

    $ sr make-purchase
