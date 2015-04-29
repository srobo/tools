ide-list-repos
==============

Synopsis
--------

``sr ide-list-repos [-h] [-t] [--server <server>] <team>``

Description
-----------

List the repositories for a team from the IDE.

Options
-------

--help, -h
    Display help and exit.

--timesort, -t
    Sort the output list by the time of the latest commit.

--server <server>, -s <server>
    The server running the IDE to connect to. This defaults to the Student
    Robotics server.

Examples
--------

.. code::

    $ sr ide-list-repos -t SRZ
