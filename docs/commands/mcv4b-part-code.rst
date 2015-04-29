mcv4b-part-code
===============

Synopsis
--------

``sr mcv4b-part-code [-h] [--wait] [-o {code,path}] [--inv-dir <inv_dir>]``

Description
-----------

Get the part code of a v4 motor board.

Note that this tool requires 'pyudev' to be installed and thus only runs on
Linux machines.

Options
-------

--help, -h
    Display help and exit.

--wait
    Wait for the MCv4b to be inserted instead of searching directly.

--output <format>, -o <format>
    Specify the output format, one of ``code`` or ``path``. Defaults to
    ``code``.

--inv-dir <dir>
    The location of the inventory. If this is not specified, it will default to
    the current working directory.

Examples
--------

.. code::

    $ sr mcv4b-part-code --wait
