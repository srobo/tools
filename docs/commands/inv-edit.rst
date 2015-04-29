inv-edit
========

Synopsis
--------

``sr inv-edit [-h] <asset_code> [<asset_code> ...]``

Description
-----------

Edit the data files of various assets in the inventory.

The editor chosen is based on your ``$EDITOR`` environment variable and falls
back to ``vim``.

Options
-------

--help, -h
    Display help and exit.

Examples
--------

.. code::

    $ sr inv-edit 000
