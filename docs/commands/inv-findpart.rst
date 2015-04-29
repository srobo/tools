inv-findpart
============

Synopsis
--------

``sr inv-findpart [-h] [-s] [-r] <asset_code> [<asset_code> ...]``

Description
-----------

Searches the inventory for an asset and gets the location of it.

Options
-------

--help, -h
    Display help and exit.

--stat, -s
    Show the status field of the assets from the 'condition' field.

--relpath, -r
    Display a relative path rather than an absolute one.

Examples
--------

.. code::

    $ sr inv-findpart -r -s 000 J1K1P
    vault/banner-sr000  working
    vault/floor/box-18l-rub-sr0H63/compartment-box-2013-srJ1K1P  unknown
