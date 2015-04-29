create-bom
==========

Synopsis
--------

``sr create-bom [-h] [--layout <layout>] <schematic> [<schematic> ...] <outfile>``

Description
-----------

Create a bill of materials. The ``outfile`` can either be an HTML or XLS file.

Options
-------

--help, -h
    Display help and exit.

--layout <layout>, -l <layout>
    The PCB layout for a single design.

Examples
--------

.. code::

    $ sr create-bom servo-v4-hw/*.sch bom.html
