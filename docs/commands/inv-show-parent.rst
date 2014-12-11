inv-show-parent
===============

Synopsis
--------

``sr inv-show-parent [-h] <asset_code> [<asset_code> ...]``

Description
-----------

Show the parents of any assets.

Options
-------

--help, -h
    Display help and exit.

Examples
--------

.. code::

    $ sr inv-show-parent 000
    # item -> parent
    000 -> dir(vault)
