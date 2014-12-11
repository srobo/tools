schedule-knockout
=================

Synopsis
--------

``sr schedule-knockout [-h] [--yaml] <number_teams>``

Description
-----------

Generate a knockout schedule for the first round.

Options
-------

--help, -h
    Display help and exit.

--yaml
    Output in YAML format.

Examples
--------

.. code::

    $ sr schedule-knockout --yaml 16
    - [0, 4, 8, 12]
    - [2, 6, 10, 14]
    - [3, 7, 11, 15]
    - [1, 5, 9, 13]
